import pandas as pd
import sqlite3

df = pd.read_csv("az_trials.csv")
conn = sqlite3.connect("az_trials.db")
df.to_sql("trials", conn, if_exists="replace", index=False)
conn.close()
print("Loaded into az_trials.db")