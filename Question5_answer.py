import json
import sqlite3
import pandas as pd

# Load JSON file
with open("Sample_Data.json") as f:
    data = json.load(f)

customers = []
transactions = []

# Extract data from transactions
for txn in data.get("transactions", []):
    person = txn.get("individual", {})
    person_id = person.get("refID", "unknown")

    # Add customer
    customers.append({
        "person_id": person_id,
        "first_name": person.get("firstname", ""),
        "last_name": person.get("surname", ""),
        "date_of_birth": person.get("dateOfBirth", ""),
        "occupation": person.get("occupation", "")
    })

    # Debug: print location_id to inspect
    print("Extracted location_id:", txn.get("reportingEntityLocationId", ""))

    # Add transaction
    transactions.append({
        "txn_id": txn.get("transactionId") or f"txn_auto_{len(transactions)+1}",
        "amount": txn.get("transactionAmount", 0),
        "currency": txn.get("transactionCurrency", ""),
        "transaction_date": txn.get("transactionDate", ""),
        "location_id": txn.get("reportingEntityLocationId", ""),
        "person_id": person_id
    })

# Connect to SQLite
conn = sqlite3.connect("lctr.db")
cursor = conn.cursor()

# Create tables
cursor.execute("""
CREATE TABLE IF NOT EXISTS Customers(
    person_id TEXT PRIMARY KEY,
    first_name TEXT,
    last_name TEXT,
    date_of_birth TEXT,
    occupation TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS Transactions(
    txn_id TEXT PRIMARY KEY,
    amount REAL,
    currency TEXT,
    transaction_date TEXT,
    location_id TEXT,
    person_id TEXT,
    FOREIGN KEY(person_id) REFERENCES Customers(person_id)
)
""")

# Clear existing data to avoid primary key errors
cursor.execute("DELETE FROM Transactions")
cursor.execute("DELETE FROM Customers")

# Insert into tables
pd.DataFrame(customers).drop_duplicates(subset="person_id").to_sql("Customers", conn, if_exists="append", index=False)
pd.DataFrame(transactions).drop_duplicates(subset="txn_id").to_sql("Transactions", conn, if_exists="append", index=False)

print("Data loaded into SQLite database 'lctr.db'.")

conn.commit()
conn.close()
