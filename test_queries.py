import sqlite3

conn = sqlite3.connect("az_trials.db")

queries = {
    "trials_by_phase": "SELECT phase, COUNT(*) as trial_count FROM trials WHERE status IN ('RECRUITING','ACTIVE_NOT_RECRUITING') GROUP BY phase;",
    "overdue_trials": "SELECT nct_id, title, completion_date, status FROM trials WHERE completion_date < date('now') AND status NOT IN ('COMPLETED','TERMINATED');",
    "top_conditions": "SELECT condition, COUNT(*) as trial_count FROM trials WHERE status IN ('RECRUITING','ACTIVE_NOT_RECRUITING') GROUP BY condition ORDER BY trial_count DESC LIMIT 10;"
}

for name, sql in queries.items():
    print(f"\n--- {name} ---")
    cursor = conn.execute(sql)
    for row in cursor.fetchall():
        print(row)

conn.close()