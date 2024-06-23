from flask import Flask, request, jsonify
from dotenv import load_dotenv
import os
import openai
import libsql_experimental as libsql
import json
import random
import requests
# Load environment variables
load_dotenv()

# Database connection setup
url = os.getenv("TURSO_DATABASE_URL")
auth_token = os.getenv("TURSO_AUTH_TOKEN")
conn = libsql.connect("quizzical.db", sync_url=url, auth_token=auth_token)
conn.sync()

# Flask app setup
app = Flask(__name__)

# Load additional environment variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY

question_generation_agent_prompt = """
You are an expert in environmental science education, tasked with creating questions to assess the mastery of various essential knowledge points related to environmental science.

Your job is to create questions that will test the student's knowledge and understanding of specific essential knowledge points. 

The list of potential essential knowledge points and their descriptions are the following:

- STB-4.A.1: The stratospheric ozone layer is important to the evolution of life on Earth and the continued health and survival of life on Earth.
- STB-4.A.2: Stratospheric ozone depletion is caused by anthropogenic factors, such as chlorofluorocarbons (CFCs), and natural factors, such as the melting of ice crystals in the atmosphere at the beginning of the Antarctic spring.
- STB-4.A.3: A decrease in stratospheric ozone increases the UV rays that reach the Earth’s surface. Exposure to UV rays can lead to skin cancer and cataracts in humans.
- STB-4.B.1: Ozone depletion can be mitigated by replacing ozone-depleting chemicals with substitutes that do not deplete the ozone layer. Hydrofluorocarbons (HFCs) are one such replacement, but some are strong greenhouse gases.
- STB-4.C.1: The principal greenhouse gases are carbon dioxide, methane, water vapor, nitrous oxide, and chlorofluorocarbons (CFCs).
- STB-4.C.2: While water vapor is a greenhouse gas, it doesn’t contribute significantly to global climate change because it has a short residence time in the atmosphere.
- STB-4.C.3: The greenhouse effect results in the surface temperature necessary for life on Earth to exist.
- STB-4.D.1: Carbon dioxide, which has a global warming potential (GWP) of 1, is used as a reference point for the comparison of different greenhouse gases and their impacts on global climate change. Chlorofluorocarbons (CFCs) have the highest GWP, followed by nitrous oxide, then methane.
- STB-4.E.1: Global climate change, caused by excess greenhouse gases in the atmosphere, can lead to a variety of environmental problems including rising sea levels resulting from melting ice sheets and ocean water expansion, and disease vectors spreading from the tropics toward the poles. These problems can lead to changes in population dynamics and population movements in response.
- STB-4.F.1: The Earth has undergone climate change throughout geologic time, with major shifts in global temperatures causing periods of warming and cooling as recorded with CO2 data and ice cores.
- STB-4.F.2: Effects of climate change include rising temperatures, melting permafrost and sea ice, rising sea levels, and displacement of coastal populations.
- STB-4.F.3: Marine ecosystems are affected by changes in sea level, some positively, such as in newly created habitats on now-flooded continental shelves, and some negatively, such as deeper communities that may no longer be in the photic zone of seawater.
- STB-4.F.4: Winds generated by atmospheric circulation help transport heat throughout the Earth. Climate change may change circulation patterns, as temperature changes may impact Hadley cells and the jet stream.
- STB-4.F.5: Oceanic currents, or the ocean conveyor belt, carry heat throughout the world. When these currents change, it can have a big impact on global climate, especially in coastal regions.
- STB-4.F.6: Climate change can affect soil through changes in temperature and rainfall, which can impact soil’s viability and potentially increase erosion.
- STB-4.F.7: Earth’s polar regions are showing faster response times to global climate change because ice and snow in these regions reflect the most energy back out to space, leading to a positive feedback loop.
- STB-4.F.8: As the Earth warms, this ice and snow melts, meaning less solar energy is radiated back into space and instead is absorbed by the Earth’s surface. This in turn causes more warming of the polar regions.
- STB-4.F.9: Global climate change response time in the Arctic is due to positive feedback loops involving melting sea ice and thawing tundra, and the subsequent release of greenhouse gases like methane.
- STB-4.F.10: One consequence of the loss of ice and snow in polar regions is the effect on species that depend on the ice for habitat and food.
- STB-4.G.1: Ocean warming is caused by the increase in greenhouse gases in the atmosphere.
- STB-4.G.2: Ocean warming can affect marine species in a variety of ways, including loss of habitat, and metabolic and reproductive changes.
- STB-4.G.3: Ocean warming is causing coral bleaching, which occurs when the loss of algae within corals cause the corals to bleach white. Some corals recover and some die.
- STB-4.H.1: Ocean acidification is the decrease in pH of the oceans, primarily due to increased CO2 concentrations in the atmosphere, and can be expressed as chemical equations.
- STB-4.H.2: As more CO2 is released into the atmosphere, the oceans, which absorb a large part of that CO2, become more acidic.
- STB-4.H.3: Anthropogenic activities that contribute to ocean acidification are those that lead to increased CO2 concentrations in the atmosphere: burning of fossil fuels, vehicle emissions, and deforestation.
- STB-4.H.4: Ocean acidification damages coral because acidification makes it difficult for them to form shells, due to the loss of calcium carbonate.
- EIN-4.A.1: Invasive species are species that can live, and sometimes thrive, outside of their normal habitat. Invasive species can sometimes be beneficial, but they are considered invasive when they threaten native species.
- EIN-4.A.2: Invasive species are often generalist, r-selected species and therefore may outcompete native species for resources.
- EIN-4.A.3: Invasive species can be controlled through a variety of human interventions.
- EIN-4.B.1: A variety of factors can lead to a species becoming threatened with extinction, such as being extensively hunted, having a limited diet, being outcompeted by invasive species, or having specific and limited habitat requirements.
- EIN-4.B.2: Not all species will be in danger of extinction when exposed to the same changes in their ecosystem. Species that are able to adapt to changes in their environment or that are able to move to a new environment are less likely to face extinction.
- EIN-4.B.3: Selective pressures are any factors that change the behaviors and fitness of organisms within an environment.
- EIN-4.B.4: Species in a given ecosystem compete for resources like territory, food, mates, and habitat, and this competition may lead to endangerment or extinction.
- EIN-4.B.5: Strategies to protect animal populations include criminalizing poaching, protecting animal habitats, and legislation.
- EIN-4.C.1: HIPPCO (habitat destruction, invasive species, population growth, pollution, climate change, and overexploitation) describes the main factors leading to a decrease in biodiversity.
- EIN-4.C.2: Habitat fragmentation occurs when large habitats are broken into smaller, isolated areas. Causes of habitat fragmentation include the construction of roads and pipelines, clearing for agriculture or development, and logging.
- EIN-4.C.3: The scale of habitat fragmentation that has an adverse effect on the inhabitants of a given ecosystem will vary from species to species within that ecosystem.
- EIN-4.C.4: Global climate change can cause habitat loss via changes in temperature, precipitation, and sea level rise.
- EIN-4.C.5: Some organisms have been somewhat or completely domesticated and are now managed for economic returns, such as honeybee colonies and domestic livestock. This domestication can have a negative impact on the biodiversity of that organism.
- EIN-4.C.6: Some ways humans can mitigate the impact of loss of biodiversity include creating protected areas, use of habitat corridors, promoting sustainable land use practices, and restoring lost habitats.

You will create a question that will assess the student's mastery of the specified essential knowledge point. 

Be thorough and ensure that the questions created are challenging and require a deep understanding of the essential knowledge to answer correctly.

The question should NEVER be a simple knowledge check where memorization is all that is required. 

The question should require critical thinking and creativity. 

DO NOT include the essential knowledge code or description in the question.


You will receive an essential knowledge code and its description in the format:
Essential Knowledge Code: (some essential knowledge code)
Description: (some essential knowledge description)


You will then output the question in a JSON format.
For example, if given the essential knowledge STB-4.A.1:
Essential Knowledge Code: STB-4.A.1
Description: The stratospheric ozone layer is important to the evolution of life on Earth and the continued health and survival of life on Earth.

Your output should be:
{
 "essential_knowledge_code": "STB-4.A.1",
 "question": (some question)
}

"""

grader_prompt = """
You are a supervisor managing a set of essential knowledge points and their associated mastery scores in a database.

Your job is to add or subtract points to a specific essential knowledge point based on the question and answer of a student.

You will receive a question, answer, and essential knowledge code in the format:
Q: (some question)
A: (some answer)
Essential Knowledge Code: (some essential knowledge code)

You will then assess whether the student demonstrated the essential knowledge associated with the essential knowledge code provided.

You will then output the result in a json format.
For example, if the student demonstrated the essential knowledge, the output should be:
{
 "STB-4.A.1": 1
}
If the student failed to demonstrate the essential knowledge, the output should be:
{
 "STB-4.A.1": -1
}
Always give 1 or -1, only put -1 if the question tests for the essential knowledge and the student failed to demonstrate it. 
You are a strict grader, to gain points for any essential knowledge, the answer must demonstrate a deep understanding of the essential knowledge, a short simple answer is not enough.
You are conservative about what essential knowledge the questions and answers demonstrate, only update if the question and answer really fit/demonstrate the essential knowledge.

The list of essential knowledge points is as follows:
- STB-4.A.1: The stratospheric ozone layer is important to the evolution of life on Earth and the continued health and survival of life on Earth.
- STB-4.A.2: Stratospheric ozone depletion is caused by anthropogenic factors, such as chlorofluorocarbons (CFCs), and natural factors, such as the melting of ice crystals in the atmosphere at the beginning of the Antarctic spring.
- STB-4.A.3: A decrease in stratospheric ozone increases the UV rays that reach the Earth’s surface. Exposure to UV rays can lead to skin cancer and cataracts in humans.
- STB-4.B.1: Ozone depletion can be mitigated by replacing ozone-depleting chemicals with substitutes that do not deplete the ozone layer. Hydrofluorocarbons (HFCs) are one such replacement, but some are strong greenhouse gases.
- STB-4.C.1: The principal greenhouse gases are carbon dioxide, methane, water vapor, nitrous oxide, and chlorofluorocarbons (CFCs).
- STB-4.C.2: While water vapor is a greenhouse gas, it doesn’t contribute significantly to global climate change because it has a short residence time in the atmosphere.
- STB-4.C.3: The greenhouse effect results in the surface temperature necessary for life on Earth to exist.
- STB-4.D.1: Carbon dioxide, which has a global warming potential (GWP) of 1, is used as a reference point for the comparison of different greenhouse gases and their impacts on global climate change. Chlorofluorocarbons (CFCs) have the highest GWP, followed by nitrous oxide, then methane.
- STB-4.E.1: Global climate change, caused by excess greenhouse gases in the atmosphere, can lead to a variety of environmental problems including rising sea levels resulting from melting ice sheets and ocean water expansion, and disease vectors spreading from the tropics toward the poles. These problems can lead to changes in population dynamics and population movements in response.
- STB-4.F.1: The Earth has undergone climate change throughout geologic time, with major shifts in global temperatures causing periods of warming and cooling as recorded with CO2 data and ice cores.
- STB-4.F.2: Effects of climate change include rising temperatures, melting permafrost and sea ice, rising sea levels, and displacement of coastal populations.
- STB-4.F.3: Marine ecosystems are affected by changes in sea level, some positively, such as in newly created habitats on now-flooded continental shelves, and some negatively, such as deeper communities that may no longer be in the photic zone of seawater.
- STB-4.F.4: Winds generated by atmospheric circulation help transport heat throughout the Earth. Climate change may change circulation patterns, as temperature changes may impact Hadley cells and the jet stream.
- STB-4.F.5: Oceanic currents, or the ocean conveyor belt, carry heat throughout the world. When these currents change, it can have a big impact on global climate, especially in coastal regions.
- STB-4.F.6: Climate change can affect soil through changes in temperature and rainfall, which can impact soil’s viability and potentially increase erosion.
- STB-4.F.7: Earth’s polar regions are showing faster response times to global climate change because ice and snow in these regions reflect the most energy back out to space, leading to a positive feedback loop.
- STB-4.F.8: As the Earth warms, this ice and snow melts, meaning less solar energy is radiated back into space and instead is absorbed by the Earth’s surface. This in turn causes more warming of the polar regions.
- STB-4.F.9: Global climate change response time in the Arctic is due to positive feedback loops involving melting sea ice and thawing tundra, and the subsequent release of greenhouse gases like methane.
- STB-4.F.10: One consequence of the loss of ice and snow in polar regions is the effect on species that depend on the ice for habitat and food.
- STB-4.G.1: Ocean warming is caused by the increase in greenhouse gases in the atmosphere.
- STB-4.G.2: Ocean warming can affect marine species in a variety of ways, including loss of habitat, and metabolic and reproductive changes.
- STB-4.G.3: Ocean warming is causing coral bleaching, which occurs when the loss of algae within corals cause the corals to bleach white. Some corals recover and some die.
- STB-4.H.1: Ocean acidification is the decrease in pH of the oceans, primarily due to increased CO2 concentrations in the atmosphere, and can be expressed as chemical equations.
- STB-4.H.2: As more CO2 is released into the atmosphere, the oceans, which absorb a large part of that CO2, become more acidic.
- STB-4.H.3: Anthropogenic activities that contribute to ocean acidification are those that lead to increased CO2 concentrations in the atmosphere: burning of fossil fuels, vehicle emissions, and deforestation.
- STB-4.H.4: Ocean acidification damages coral because acidification makes it difficult for them to form shells, due to the loss of calcium carbonate.
- EIN-4.A.1: Invasive species are species that can live, and sometimes thrive, outside of their normal habitat. Invasive species can sometimes be beneficial, but they are considered invasive when they threaten native species.
- EIN-4.A.2: Invasive species are often generalist, r-selected species and therefore may outcompete native species for resources.
- EIN-4.A.3: Invasive species can be controlled through a variety of human interventions.
- EIN-4.B.1: A variety of factors can lead to a species becoming threatened with extinction, such as being extensively hunted, having a limited diet, being outcompeted by invasive species, or having specific and limited habitat requirements.
- EIN-4.B.2: Not all species will be in danger of extinction when exposed to the same changes in their ecosystem. Species that are able to adapt to changes in their environment or that are able to move to a new environment are less likely to face extinction.
- EIN-4.B.3: Selective pressures are any factors that change the behaviors and fitness of organisms within an environment.
- EIN-4.B.4: Species in a given ecosystem compete for resources like territory, food, mates, and habitat, and this competition may lead to endangerment or extinction.
- EIN-4.B.5: Strategies to protect animal populations include criminalizing poaching, protecting animal habitats, and legislation.
- EIN-4.C.1: HIPPCO (habitat destruction, invasive species, population growth, pollution, climate change, and overexploitation) describes the main factors leading to a decrease in biodiversity.
- EIN-4.C.2: Habitat fragmentation occurs when large habitats are broken into smaller, isolated areas. Causes of habitat fragmentation include the construction of roads and pipelines, clearing for agriculture or development, and logging.
- EIN-4.C.3: The scale of habitat fragmentation that has an adverse effect on the inhabitants of a given ecosystem will vary from species to species within that ecosystem.
- EIN-4.C.4: Global climate change can cause habitat loss via changes in temperature, precipitation, and sea level rise.
- EIN-4.C.5: Some organisms have been somewhat or completely domesticated and are now managed for economic returns, such as honeybee colonies and domestic livestock. This domestication can have a negative impact on the biodiversity of that organism.
- EIN-4.C.6: Some ways humans can mitigate the impact of loss of biodiversity include creating protected areas, use of habitat corridors, promoting sustainable land use practices, and restoring lost habitats.

ONLY output a json file, write ABSOLUTELY nothing else
"""

answer_assessment_prompt = """
Your job is to assess a student's answer to a question in order to determine if the answer contains any details about the characteristics of the response, specifically focusing on strengths, weaknesses, or habits.

You are part of a team building a knowledge base to assist in highly customized learning plans.

You play the critical role of assessing the message to determine if it contains any information worth recording in the knowledge base.

You are only interested in the following categories of information:

Strengths
Weaknesses
Habits
You will receive the message in the format
Q: (some question)
A: (some answer)

When you see the answer, you should determine if the answer contains any information about the characteristics of the response, such as its accuracy, conciseness, depth, clarity, organization, etc.

You should ONLY RESPOND IN JSON FORMAT with STRENGTH, WEAKNESS, and HABITS. Absolutely no other information should be provided.

You should respond in short messages that are adjectives. 

Take a deep breath, think step by step, and then analyze the following message:
"""

def fetch_essential_knowledge_and_scores():
    cursor = conn.cursor()
    cursor.execute("SELECT label, knowledge, mastery_score FROM essential_knowledge")
    essential_knowledge_points = cursor.fetchall()
    cursor.close()
    return essential_knowledge_points

def choose_essential_knowledge_randomly(essential_knowledge_points):
    knowledge_codes = [point[0] for point in essential_knowledge_points]
    descriptions = [point[1] for point in essential_knowledge_points]
    scores = [point[2] for point in essential_knowledge_points]
    chosen_knowledge = random.choices(list(zip(knowledge_codes, descriptions)), weights=scores, k=1)[0]
    return chosen_knowledge

def generate_question(knowledge_code, description):
    messages = [
        {"role": "system", "content": question_generation_agent_prompt},
        {"role": "user", "content": f"Essential Knowledge Code: {knowledge_code}\nDescription: {description}"}
    ]

    response = openai.ChatCompletion.create(
        model="gpt-4-turbo",
        messages=messages,
        temperature=0.0
    )
    question_generation_response = response['choices'][0]['message']['content']
    question_json = json.loads(question_generation_response)
    return question_json["question"]

def grade_answer(question, answer, knowledge_code):
    messages = [
        {"role": "system", "content": grader_prompt},
        {"role": "user", "content": f"Q: {question}\nA: {answer}\nEssential Knowledge Code: {knowledge_code}"}
    ]

    response = openai.ChatCompletion.create(
        model="gpt-4-turbo",
        messages=messages,
        temperature=0.0
    )
    grading_response = response['choices'][0]['message']['content']
    print(grading_response)
    return json.loads(grading_response)

def assess_answer(question, answer):
    messages = [
        {"role": "system", "content": answer_assessment_prompt},
        {"role": "user", "content": f"Q: {question}\nA: {answer}"}
    ]

    response = openai.ChatCompletion.create(
        model="gpt-4-turbo",
        messages=messages,
        temperature=0.0
    )
    assessment_response = response['choices'][0]['message']['content']
    return json.loads(assessment_response)

# Define a route to generate a question based on essential knowledge code and description
@app.route("/api/generate_question")
def generate_question_route():
    essential_knowledge_points = fetch_essential_knowledge_and_scores()
    if not essential_knowledge_points:
        return jsonify({"error": "No essential knowledge points found in the database"}), 400
    
    chosen_knowledge = choose_essential_knowledge_randomly(essential_knowledge_points)
    knowledge_code, description = chosen_knowledge[0], chosen_knowledge[1]

    try:
        question = generate_question(knowledge_code, description)
        return jsonify({"essential_knowledge_code": knowledge_code, "question": question})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Define a route to generate a question for a specific essential knowledge code
@app.route("/api/generate_question/<knowledge_code>")
def generate_specific_question_route(knowledge_code):
    essential_knowledge_points = fetch_essential_knowledge_and_scores()
    knowledge_dict = {point[0]: point[1] for point in essential_knowledge_points}
    description = knowledge_dict.get(knowledge_code)
    if not description:
        return jsonify({"error": "Essential knowledge code not found"}), 404
    
    try:
        question = generate_question(knowledge_code, description)
        return jsonify({"essential_knowledge_code": knowledge_code, "question": question})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/latest_assessment")
def latest_assessment():
    cursor = conn.cursor()
    cursor.execute("""
    SELECT description FROM strengths ORDER BY id DESC LIMIT 1
    """)
    latest_strength = cursor.fetchone()

    cursor.execute("""
    SELECT description FROM weaknesses ORDER BY id DESC LIMIT 1
    """)
    latest_weakness = cursor.fetchone()

    cursor.execute("""
    SELECT description FROM habits ORDER BY id DESC LIMIT 1
    """)
    latest_habit = cursor.fetchone()
    
    cursor.close()

    if latest_strength or latest_weakness or latest_habit:
        return jsonify({
            "strengths": [latest_strength[0]] if latest_strength else [],
            "weaknesses": [latest_weakness[0]] if latest_weakness else [],
            "habits": [latest_habit[0]] if latest_habit else []
        })
    else:
        return jsonify({"error": "No assessments found"}), 404


# Define a route for grading the answer
def store_assessment_data(question, answer, knowledge_code, assessment):
    cursor = conn.cursor()
    
    strengths = assessment.get('STRENGTHS', "")
    weaknesses = assessment.get('WEAKNESS', "")
    habits = assessment.get('HABITS', "")
    print(strengths, weaknesses, habits)
    
    if strengths:
        cursor.execute("""
        INSERT INTO strengths (id, description)
        VALUES (NULL, ?)
        """, (strengths,))
    
    if weaknesses:
        cursor.execute("""
        INSERT INTO weaknesses (id, description)
        VALUES (NULL, ?)
        """, (weaknesses,))
    
    if habits:
        cursor.execute("""
        INSERT INTO habits (id, description)
        VALUES (NULL, ?)
        """, (habits,))
    
    conn.commit()
    cursor.close()

@app.route("/api/weakest_knowledge_point")
def weakest_knowledge_point():
    cursor = conn.cursor()
    cursor.execute("""
    SELECT label, knowledge
    FROM essential_knowledge
    ORDER BY mastery_score ASC
    LIMIT 1
    """)
    weakest_point = cursor.fetchone()
    cursor.close()

    if weakest_point:
        return jsonify({
            "label": weakest_point[0],
            "knowledge": weakest_point[1]
        })
    else:
        return jsonify({"error": "No essential knowledge points found"}), 404


@app.route("/api/grade_answer", methods=["POST"])
def grade_answer_route():
    data = request.json
    question = data.get("question")
    answer = data.get("answer")
    knowledge_code = data.get("essential_knowledge_code")

    if not question or not answer or not knowledge_code:
        return jsonify({"error": "Missing required fields"}), 400

    try:
        result = grade_answer(question, answer, knowledge_code)
        assessment = assess_answer(question, answer)
        # Update the mastery score in the database based on the result
        update_score(knowledge_code, result[knowledge_code])
        
        # Store assessment data in the database
        store_assessment_data(question, answer, knowledge_code, assessment)

        return jsonify({"result": result, "assessment": assessment})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def update_score(knowledge_code, score_change):
    cursor = conn.cursor()
    cursor.execute("UPDATE essential_knowledge SET mastery_score = mastery_score + ? WHERE label = ?", (score_change, knowledge_code))
    conn.commit()
    cursor.close()

YOU_API_KEY = os.getenv("YOU_API_KEY")

# Define a new route to query You.com
@app.route("/api/query_you_com", methods=["POST"])
def query_you_com():
    data = request.json
    knowledge = data.get("knowledge")

    if not knowledge:
        return jsonify({"error": "Knowledge topic is required"}), 400

    url = "https://chat-api.you.com/research"
    payload = {
        "query": f"A student is struggling in the following concepts related to AP Environmental Science: {knowledge}. Please identify different sources to help improve their skills. Try not to include more than one of the same domain name. Focus on results for AP Environmental Science or for similar classes, aimed at high school students. Some ideas are Khan academy, college board, etc.",
        "chat_id": "3c90c3cc-0d44-4b50-8888-8dd25736052a"
    }
    headers = {
        "X-API-Key": YOU_API_KEY,
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500

# Add other routes and the main entry point as needed...



@app.route("/api/learning_objectives_scores")
def learning_objectives_scores():
    cursor = conn.cursor()
    cursor.execute("""
    SELECT learning_objectives.label, AVG(essential_knowledge.mastery_score), learning_objectives.description
    FROM learning_objectives
    JOIN essential_knowledge ON learning_objectives.id = essential_knowledge.learning_objective_id
    GROUP BY learning_objectives.label
    """)
    results = cursor.fetchall()
    cursor.close()
    learning_objectives_scores = [{"learning_objective": row[0], "score": row[1]-1, "descriptions": row[2]} for row in results]
    return jsonify(learning_objectives_scores)



# Define a sample route for the Flask app
@app.route("/api/python")
def hello_world():
    return "<p>Hello, World!</p>"

if __name__ == "__main__":
    app.run(debug=True)
