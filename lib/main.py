import openai
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Set the OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

# Define the initial system prompt for the LLM
system_prompt_initial_sentinel = """
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

# Define the second system prompt for the knowledge master
system_prompt_initial_knowledge_master = """
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

def test_sentinel():
    q = "Explain the impact of deforestation on biodiversity."
    a = "Deforestation leads to the loss of habitat for many species, reducing biodiversity. It disrupts ecosystems, leading to the extinction of plants and animals that rely on forest habitats. Additionally, deforestation contributes to climate change, further threatening biodiversity."

    # combine them into a single string with appropriate labels
    messages = [f"Q: {q}", f"A: {a}"]

    response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": system_prompt_initial_sentinel},
            {"role": "user", "content": "\n".join(messages)}
        ],
        temperature=0.0
    )
    print("message:" + "\n".join(messages))
    print("Sentinel Response:")
    print(response.choices[0].message['content'])

def test_knowledge_master():
    memories = [
        "The student has strong analytical skills.",
        "The student lacks detail and depth in their explanations.",
        "The student tends to focus on key points rather than elaborating."
    ]

    q = "Explain the impact of deforestation on biodiversity."
    a = "Deforestation leads to the loss of habitat for many species, reducing biodiversity. It disrupts ecosystems, leading to the extinction of plants and animals that rely on forest habitats. Additionally, deforestation contributes to climate change, further threatening biodiversity."

    # combine them into a single string with appropriate labels
    messages = [f"Q: {q}", f"A: {a}"]
    
    response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": system_prompt_initial_knowledge_master.replace("{memories}", "\n".join(memories))},
            {"role": "user", "content": "\n".join(messages)}
        ],
        temperature=0.0
    )
    print("Knowledge Master Response:")
    print(response.choices[0].message['content'])

if __name__ == "__main__":
    test_sentinel()
    test_knowledge_master()