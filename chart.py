import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

conn = sqlite3.connect("az_trials.db")
df = pd.read_sql("SELECT phase, COUNT(*) as count FROM trials WHERE status IN ('RECRUITING','ACTIVE_NOT_RECRUITING') GROUP BY phase", conn)
conn.close()

df["phase"] = df["phase"].fillna("Not Specified").astype(str)
df.loc[df["phase"].str.strip() == "", "phase"] = "Not Specified"

plt.figure(figsize=(8,5))
plt.bar(df["phase"], df["count"])
plt.title("AstraZeneca Active Trials by Phase")
plt.xlabel("Phase")
plt.ylabel("Number of Trials")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.savefig("trials_by_phase.png")
print("Saved chart to trials_by_phase.png")