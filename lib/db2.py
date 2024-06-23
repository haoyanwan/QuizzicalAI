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
DROP TABLE IF EXISTS strengths;
DROP TABLE IF EXISTS weaknesses;
DROP TABLE IF EXISTS habits;
""")

# Create new tables with the correct schema
conn.executescript("""

CREATE TABLE IF NOT EXISTS strengths (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    description TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS weaknesses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    description TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS habits (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    description TEXT NOT NULL
);
""")

# Commit the changes
conn.commit()

# Sync the changes
conn.sync()

# Verify the data
print("Learning Objectives:")
print(conn.execute("SELECT * FROM learning_objectives").fetchall())

print("\nEssential Knowledge:")
print(conn.execute("SELECT * FROM essential_knowledge").fetchall())

print("\nStrengths:")
print(conn.execute("SELECT * FROM strengths").fetchall())

print("\nWeaknesses:")
print(conn.execute("SELECT * FROM weaknesses").fetchall())

print("\nHabits:")
print(conn.execute("SELECT * FROM habits").fetchall())
