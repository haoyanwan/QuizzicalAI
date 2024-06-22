from flask import Flask
from dotenv import load_dotenv
import os
import libsql_experimental as libsql
from langchain.pydantic_v1 import BaseModel, Field
from langchain.tools import StructuredTool
from enum import Enum
from typing import Optional
from langchain_openai.chat_models import ChatOpenAI
from langchain.prompts import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    MessagesPlaceholder,
)
from langchain_core.runnables import RunnablePassthrough
from langchain_core.utils.function_calling import convert_to_openai_function
from langgraph.prebuilt import ToolExecutor
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, ToolMessage
from langgraph.prebuilt import ToolInvocation
from typing import TypedDict, Sequence
import json

# Load environment variables
load_dotenv()

# Database connection setup
url = os.getenv("TURSO_DATABASE_URL")
auth_token = os.getenv("TURSO_AUTH_TOKEN")
conn = libsql.connect("quizzical.db", sync_url=url, auth_token=auth_token)
conn.sync()

# Flask app setup
apps = Flask(__name__)

# Load additional environment variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL")
OPENAI_ORGANIZATION = os.getenv("OPENAI_ORGANIZATION")

os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_ENDPOINT"] = "https://api.smith.langchain.com"
os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY")
os.environ["LANGCHAIN_PROJECT"] = "QuizzicalAI"

# Define enums and data models
class Category(str, Enum):
    Strength = "Strength"
    Weakness = "Weakness"
    Habits = "Habits"

class Action(str, Enum):
    Create = "Create"
    Update = "Update"
    Delete = "Delete"

class AddKnowledge(BaseModel):
    knowledge: str = Field(..., description="The knowledge to add")
    knowledge_old: Optional[str] = Field(None, description="If updating or deleting record, the complete, exact phrase that needs to be modified")
    category: Category = Field(..., description="The category of the knowledge")
    action: Action = Field(..., description="Whether this knowledge is adding a new record, updating a record, or deleting a record")

# Define the function to modify knowledge
def modify_knowledge(knowledge: str, category: str, action: str, knowledge_old: str = "") -> dict:
    print("Modifying knowledge: ", knowledge, category, action, knowledge_old)
    return {
        "knowledge": knowledge,
        "category": category,
        "action": action,
        "knowledge_old": knowledge_old
    }

# Define the StructuredTool for modifying knowledge
tool_modify_knowledge = StructuredTool.from_function(
    func=modify_knowledge,
    name="Knowledge_Modifier",
    description="Add, update, or delete a bit of knowledge",
    args_schema=AddKnowledge,
)

# Define the initial system prompt for the LLM
system_prompt_initial = """
Your job is to assess a student's answer towards a question in order to determine if the student's answer contains any details about a student's weaknesses, strengths, or habits.

You are part of a team building a knowledge base to assist in highly customized learning plans.

You play the critical role of assessing the message to determine if it contains any information worth recording in the knowledge base.

You are only interested in the following categories of information:

1. Strengths
2. Weaknesses
3. Habits

You will receive the a message in the format
Q: (some question)
A: (some answer)

When you see the answer, you should determine if the answer contains any information about the student's strengths, weaknesses, or habits.

You should ONLY RESPOND IN JSON FORMAT with STRENGTH, WEAKNESS, and HABITS. Absolutely no other information should be provided.

Take a deep breath, think step by step, and then analyze the following message:
"""

# Create the prompt template
prompt = ChatPromptTemplate.from_messages(
    [
        SystemMessagePromptTemplate.from_template(system_prompt_initial),
        MessagesPlaceholder(variable_name="messages"),
        (
            "system",
            "Remember, only respond IN JSON FORMAT with STRENGTH, WEAKNESS, and HABITS. Do not provide any other information.",
        ),
    ]
)

# Choose the LLM that will drive the agent
llm = ChatOpenAI(
    model="gpt-4o",
    streaming=True,
    temperature=0.0,
)

sentinel_runnable = {"messages": RunnablePassthrough()} | prompt | llm

# Define the second system prompt for the knowledge master
system_prompt_initial = """
You are a supervisor managing a team of knowledge experts.

Your team's job is to create a perfect knowledge base about a student's strengths, weaknesses, and habits.

The knowledge base should ultimately consist of many pieces of information about the student's strengths, weaknesses, and habits, e.g., "The student has strong analytical skills." or "The student lacks detail and depth in their explanations." or "The student tends to focus on key points rather than elaborating."

Every time you receive a message, you will evaluate if it has any information worth recording in the knowledge base.

A message may contain multiple pieces of information that should be saved separately.

You are only interested in the following categories of information:

1. Strengths
2. Weaknesses
3. Habits

When you receive a message, you perform a sequence of steps consisting of:

1. Analyze the most recent Human message for information. You will see multiple messages for context, but we are only looking for new information in the most recent message.
2. Compare this to the knowledge you already have.
3. Determine if this is new knowledge, an update to old knowledge that now needs to change, or should result in deleting information that is not correct. It's possible that a piece of information previously recorded as a strength might now be a weakness, or that a habit previously noted might have changed - those examples would require an update.

Here are the existing bits of information that we have about the student:

'''
{memories}
'''


Call the right tools to save the information, then respond with DONE. If you identify multiple pieces of information, call everything at once. You only have one chance to call tools.

I will tip you $20 if you are perfect, and I will fine you $40 if you miss any important information or change any incorrect information.

Take a deep breath, think step by step, and then analyze the following message:
"""

# Create the knowledge master prompt template
prompt = ChatPromptTemplate.from_messages(
    [
        SystemMessagePromptTemplate.from_template(system_prompt_initial),
        MessagesPlaceholder(variable_name="messages"),
    ]
)

# Choose the LLM for the knowledge master
llm = ChatOpenAI(
    model="gpt-4o",
    streaming=True,
    temperature=0.0,
)

# Set up the tools to execute them from the graph
agent_tools = [tool_modify_knowledge]
tool_executor = ToolExecutor(agent_tools)

# Create the tools to bind to the model
tools = [convert_to_openai_function(t) for t in agent_tools]
knowledge_master_runnable = prompt | llm.bind_tools(tools)

# Define the AgentState class
class AgentState(TypedDict):
    messages: Sequence[BaseMessage]
    memories: Sequence[str]
    contains_information: str

# Define the function to call the sentinel
def call_sentinel(state):
    messages = state["messages"]
    response = sentinel_runnable.invoke(messages)
    return response

# Define the function to determine whether to continue or not
def should_continue(state):
    last_message = state["messages"][-1]
    if "tool_calls" not in last_message.additional_kwargs:
        return "end"
    else:
        return "continue"

# Define the function to call the knowledge master
def call_knowledge_master(state):
    messages = state["messages"]
    memories = state["memories"]
    response = knowledge_master_runnable.invoke(
        {"messages": messages, "memories": memories}
    )
    return {"messages": messages + [response]}

# Define the function to execute tools
def call_tool(state):
    messages = state["messages"]
    last_message = messages[-1]
    for tool_call in last_message.additional_kwargs["tool_calls"]:
        action = ToolInvocation(
            tool=tool_call["function"]["name"],
            tool_input=json.loads(tool_call["function"]["arguments"]),
            id=tool_call["id"],
        )
        response = tool_executor.invoke(action)
        function_message = ToolMessage(
            content=str(response), name=action.tool, tool_call_id=tool_call["id"]
        )
        messages.append(function_message)
    return {"messages": messages}

from langgraph.graph import StateGraph, END

# Initialize a new graph
graph = StateGraph(AgentState)

# Define the nodes in the graph
graph.add_node("sentinel", call_sentinel)
graph.add_node("knowledge_master", call_knowledge_master)
graph.add_node("action", call_tool)

# Set the entry point
graph.set_entry_point("sentinel")

# Add conditional edges
graph.add_conditional_edges(
    "sentinel",
    lambda x: x["contains_information"],
    {
        "yes": "knowledge_master",
        "no": END,
    },
)
graph.add_conditional_edges(
    "knowledge_master",
    should_continue,
    {
        "continue": "action",
        "end": END,
    },
)

# Add normal edges
graph.add_edge("action", END)

# Compile the workflow as a runnable
app = graph.compile()

# Test the workflow with a sample input
message_robot = "Explain the impact of deforestation on biodiversity."
message_human = "Deforestation leads to the loss of habitat for many species, reducing biodiversity. It disrupts ecosystems, leading to the extinction of plants and animals that rely on forest habitats. Additionally, deforestation contributes to climate change, further threatening biodiversity."
inputs = {
    "messages": [
        AIMessage(content=message_robot),
        HumanMessage(content=message_human),
    ],
}

for output in app.with_config({"run_name": "Memory"}).stream(inputs):
    for key, value in output.items():
        print(f"Output from node '{key}':")
        print("---")
        print(value)
    print("\n---\n")

# Define a sample route for the Flask app
@apps.route("/api/python")
def hello_world():
    return "<p>Hello, World!</p>"

if __name__ == "__main__":
    apps.run(debug=True)
