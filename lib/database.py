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
DROP TABLE IF EXISTS student;
DROP TABLE IF EXISTS skills;
DROP TABLE IF EXISTS traits;
""")

# Create tables with the correct schema
conn.executescript("""
CREATE TABLE IF NOT EXISTS student (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS skills (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    label TEXT NOT NULL UNIQUE,
    name TEXT NOT NULL,
    mastery_score FLOAT DEFAULT 0.0,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS traits (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    label TEXT NOT NULL,
    description TEXT
);
""")

# Insert sample data
conn.executescript("""
-- Insert student data
INSERT OR REPLACE INTO student (id, name, email) VALUES 
(1, 'John Doe', 'john@example.com');

-- Insert skills data
INSERT OR REPLACE INTO skills (label, name) VALUES 
('1.A', 'Describe environmental concepts and processes.'),
('1.B', 'Explain environmental concepts and processes.'),
('1.C', 'Explain environmental concepts, processes, or models in applied contexts.'),
('2.A', 'Describe characteristics of an environmental concept, process, or model represented visually.'),
('2.B', 'Explain relationships between different characteristics of environmental concepts, processes, or models represented visually: In theoretical contexts, In applied contexts'),
('2.C', 'Explain how environmental concepts and processes represented visually relate to broader environmental issues.'),
('3.A', 'Identify the author''s claim.'),
('3.B', 'Describe the author''s perspective and assumptions.'),
('3.C', 'Describe the author''s reasoning (use of evidence to support a claim).'),
('3.D', 'Evaluate the credibility of a source: Recognize bias, Scientific accuracy'),
('3.E', 'Evaluate the validity of conclusions of a source or research study.'),
('4.A', 'Identify a testable hypothesis or scientific question for an investigation.'),
('4.B', 'Identify a research method, design, and/or measure used.'),
('4.C', 'Describe an aspect of a research method, design, and/or measure used.'),
('4.D', 'Make observations or collect data from laboratory setups.'),
('4.E', 'Explain modifications to an experimental procedure that will alter results.');
""")

# Commit the changes
conn.commit()

# Sync the changes
conn.sync()

# Verify the data
print("Student:")
print(conn.execute("SELECT * FROM student").fetchall())

print("\nSkills:")
print(conn.execute("SELECT * FROM skills").fetchall())

print("\nTraits:")
print(conn.execute("SELECT * FROM traits").fetchall())
