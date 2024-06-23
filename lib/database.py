import libsql_experimental as libsql
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

url = os.getenv("TURSO_DATABASE_URL")
auth_token = os.getenv("TURSO_AUTH_TOKEN")

# Connect to the database
conn = libsql.connect("quizzical.db", sync_url=url, auth_token=auth_token)
conn.sync()

# Drop existing tables if they exist
conn.executescript("""
DROP TABLE IF EXISTS learning_objectives;
DROP TABLE IF EXISTS essential_knowledge;
""")

# Create new tables with the correct schema
conn.executescript("""
CREATE TABLE IF NOT EXISTS learning_objectives (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    label TEXT NOT NULL UNIQUE,
    description TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS essential_knowledge (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    label TEXT NOT NULL UNIQUE,
    knowledge TEXT NOT NULL,
    learning_objective_id INTEGER NOT NULL,
    mastery_score INTEGER DEFAULT 1,
    FOREIGN KEY (learning_objective_id) REFERENCES learning_objectives(id)
);
""")

# Insert learning objectives data
learning_objectives_data = [
    ('STB-4.A', 'Explain the importance of stratospheric ozone to life on Earth.'),
    ('STB-4.B', 'Describe chemicals used to substitute for chlorofluorocarbons (CFCs).'),
    ('STB-4.C', 'Identify the greenhouse gases.'),
    ('STB-4.D', 'Identify the sources and potency of the greenhouse gases.'),
    ('STB-4.E', 'Identify the threats to human health and the environment posed by an increase in greenhouse gases.'),
    ('STB-4.F', 'Explain how changes in climate, both short- and long-term, impact ecosystems.'),
    ('STB-4.G', 'Explain the causes and effects of ocean warming.'),
    ('STB-4.H', 'Explain the causes and effects of ocean acidification.'),
    ('EIN-4.A', 'Explain the environmental problems associated with invasive species and strategies to control them.'),
    ('EIN-4.B', 'Explain how species become endangered and strategies to combat the problem.'),
    ('EIN-4.C', 'Explain how human activities affect biodiversity and strategies to combat the problem.')
]

conn.executemany("INSERT OR REPLACE INTO learning_objectives (label, description) VALUES (?, ?);", learning_objectives_data)

# Retrieve the learning objective IDs
learning_objectives = {label: id for id, label in conn.execute("SELECT id, label FROM learning_objectives").fetchall()}

# Insert essential knowledge data
essential_knowledge_data = [
    ('STB-4.A.1', 'The stratospheric ozone layer is important to the evolution of life on Earth and the continued health and survival of life on Earth.', learning_objectives['STB-4.A']),
    ('STB-4.A.2', 'Stratospheric ozone depletion is caused by anthropogenic factors, such as chlorofluorocarbons (CFCs), and natural factors, such as the melting of ice crystals in the atmosphere at the beginning of the Antarctic spring.', learning_objectives['STB-4.A']),
    ('STB-4.A.3', 'A decrease in stratospheric ozone increases the UV rays that reach the Earth’s surface. Exposure to UV rays can lead to skin cancer and cataracts in humans.', learning_objectives['STB-4.A']),
    ('STB-4.B.1', 'Ozone depletion can be mitigated by replacing ozone-depleting chemicals with substitutes that do not deplete the ozone layer. Hydrofluorocarbons (HFCs) are one such replacement, but some are strong greenhouse gases.', learning_objectives['STB-4.B']),
    ('STB-4.C.1', 'The principal greenhouse gases are carbon dioxide, methane, water vapor, nitrous oxide, and chlorofluorocarbons (CFCs).', learning_objectives['STB-4.C']),
    ('STB-4.C.2', 'While water vapor is a greenhouse gas, it doesn’t contribute significantly to global climate change because it has a short residence time in the atmosphere.', learning_objectives['STB-4.C']),
    ('STB-4.C.3', 'The greenhouse effect results in the surface temperature necessary for life on Earth to exist.', learning_objectives['STB-4.C']),
    ('STB-4.D.1', 'Carbon dioxide, which has a global warming potential (GWP) of 1, is used as a reference point for the comparison of different greenhouse gases and their impacts on global climate change. Chlorofluorocarbons (CFCs) have the highest GWP, followed by nitrous oxide, then methane.', learning_objectives['STB-4.D']),
    ('STB-4.E.1', 'Global climate change, caused by excess greenhouse gases in the atmosphere, can lead to a variety of environmental problems including rising sea levels resulting from melting ice sheets and ocean water expansion, and disease vectors spreading from the tropics toward the poles. These problems can lead to changes in population dynamics and population movements in response.', learning_objectives['STB-4.E']),
    ('STB-4.F.1', 'The Earth has undergone climate change throughout geologic time, with major shifts in global temperatures causing periods of warming and cooling as recorded with CO2 data and ice cores.', learning_objectives['STB-4.F']),
    ('STB-4.F.2', 'Effects of climate change include rising temperatures, melting permafrost and sea ice, rising sea levels, and displacement of coastal populations.', learning_objectives['STB-4.F']),
    ('STB-4.F.3', 'Marine ecosystems are affected by changes in sea level, some positively, such as in newly created habitats on now-flooded continental shelves, and some negatively, such as deeper communities that may no longer be in the photic zone of seawater.', learning_objectives['STB-4.F']),
    ('STB-4.F.4', 'Winds generated by atmospheric circulation help transport heat throughout the Earth. Climate change may change circulation patterns, as temperature changes may impact Hadley cells and the jet stream.', learning_objectives['STB-4.F']),
    ('STB-4.F.5', 'Oceanic currents, or the ocean conveyor belt, carry heat throughout the world. When these currents change, it can have a big impact on global climate, especially in coastal regions.', learning_objectives['STB-4.F']),
    ('STB-4.F.6', 'Climate change can affect soil through changes in temperature and rainfall, which can impact soil’s viability and potentially increase erosion.', learning_objectives['STB-4.F']),
    ('STB-4.F.7', 'Earth’s polar regions are showing faster response times to global climate change because ice and snow in these regions reflect the most energy back out to space, leading to a positive feedback loop.', learning_objectives['STB-4.F']),
    ('STB-4.F.8', 'As the Earth warms, this ice and snow melts, meaning less solar energy is radiated back into space and instead is absorbed by the Earth’s surface. This in turn causes more warming of the polar regions.', learning_objectives['STB-4.F']),
    ('STB-4.F.9', 'Global climate change response time in the Arctic is due to positive feedback loops involving melting sea ice and thawing tundra, and the subsequent release of greenhouse gases like methane.', learning_objectives['STB-4.F']),
    ('STB-4.F.10', 'One consequence of the loss of ice and snow in polar regions is the effect on species that depend on the ice for habitat and food.', learning_objectives['STB-4.F']),
    ('STB-4.G.1', 'Ocean warming is caused by the increase in greenhouse gases in the atmosphere.', learning_objectives['STB-4.G']),
    ('STB-4.G.2', 'Ocean warming can affect marine species in a variety of ways, including loss of habitat, and metabolic and reproductive changes.', learning_objectives['STB-4.G']),
    ('STB-4.G.3', 'Ocean warming is causing coral bleaching, which occurs when the loss of algae within corals cause the corals to bleach white. Some corals recover and some die.', learning_objectives['STB-4.G']),
    ('STB-4.H.1', 'Ocean acidification is the decrease in pH of the oceans, primarily due to increased CO2 concentrations in the atmosphere, and can be expressed as chemical equations.', learning_objectives['STB-4.H']),
    ('STB-4.H.2', 'As more CO2 is released into the atmosphere, the oceans, which absorb a large part of that CO2, become more acidic.', learning_objectives['STB-4.H']),
    ('STB-4.H.3', 'Anthropogenic activities that contribute to ocean acidification are those that lead to increased CO2 concentrations in the atmosphere: burning of fossil fuels, vehicle emissions, and deforestation.', learning_objectives['STB-4.H']),
    ('STB-4.H.4', 'Ocean acidification damages coral because acidification makes it difficult for them to form shells, due to the loss of calcium carbonate.', learning_objectives['STB-4.H']),
    ('EIN-4.A.1', 'Invasive species are species that can live, and sometimes thrive, outside of their normal habitat. Invasive species can sometimes be beneficial, but they are considered invasive when they threaten native species.', learning_objectives['EIN-4.A']),
    ('EIN-4.A.2', 'Invasive species are often generalist, r-selected species and therefore may outcompete native species for resources.', learning_objectives['EIN-4.A']),
    ('EIN-4.A.3', 'Invasive species can be controlled through a variety of human interventions.', learning_objectives['EIN-4.A']),
    ('EIN-4.B.1', 'A variety of factors can lead to a species becoming threatened with extinction, such as being extensively hunted, having a limited diet, being outcompeted by invasive species, or having specific and limited habitat requirements.', learning_objectives['EIN-4.B']),
    ('EIN-4.B.2', 'Not all species will be in danger of extinction when exposed to the same changes in their ecosystem. Species that are able to adapt to changes in their environment or that are able to move to a new environment are less likely to face extinction.', learning_objectives['EIN-4.B']),
    ('EIN-4.B.3', 'Selective pressures are any factors that change the behaviors and fitness of organisms within an environment.', learning_objectives['EIN-4.B']),
    ('EIN-4.B.4', 'Species in a given ecosystem compete for resources like territory, food, mates, and habitat, and this competition may lead to endangerment or extinction.', learning_objectives['EIN-4.B']),
    ('EIN-4.B.5', 'Strategies to protect animal populations include criminalizing poaching, protecting animal habitats, and legislation.', learning_objectives['EIN-4.B']),
    ('EIN-4.C.1', 'HIPPCO (habitat destruction, invasive species, population growth, pollution, climate change, and overexploitation) describes the main factors leading to a decrease in biodiversity.', learning_objectives['EIN-4.C']),
    ('EIN-4.C.2', 'Habitat fragmentation occurs when large habitats are broken into smaller, isolated areas. Causes of habitat fragmentation include the construction of roads and pipelines, clearing for agriculture or development, and logging.', learning_objectives['EIN-4.C']),
    ('EIN-4.C.3', 'The scale of habitat fragmentation that has an adverse effect on the inhabitants of a given ecosystem will vary from species to species within that ecosystem.', learning_objectives['EIN-4.C']),
    ('EIN-4.C.4', 'Global climate change can cause habitat loss via changes in temperature, precipitation, and sea level rise.', learning_objectives['EIN-4.C']),
    ('EIN-4.C.5', 'Some organisms have been somewhat or completely domesticated and are now managed for economic returns, such as honeybee colonies and domestic livestock. This domestication can have a negative impact on the biodiversity of that organism.', learning_objectives['EIN-4.C']),
    ('EIN-4.C.6', 'Some ways humans can mitigate the impact of loss of biodiversity include creating protected areas, use of habitat corridors, promoting sustainable land use practices, and restoring lost habitats.', learning_objectives['EIN-4.C'])
]

conn.executemany("INSERT OR REPLACE INTO essential_knowledge (label, knowledge, learning_objective_id, mastery_score) VALUES (?, ?, ?, 1);", essential_knowledge_data)

# Commit the changes
conn.commit()

# Sync the changes
conn.sync()

# Verify the data
print("Learning Objectives:")
print(conn.execute("SELECT * FROM learning_objectives").fetchall())

print("\nEssential Knowledge:")
print(conn.execute("SELECT * FROM essential_knowledge").fetchall())
