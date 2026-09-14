import os
import sqlite3
import google.generativeai as genai
from dotenv import load_dotenv
load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-flash-lite-latest")

QUERIES = {
    "trials_by_phase": "SELECT phase, COUNT(*) as trial_count FROM trials WHERE status IN ('RECRUITING','ACTIVE_NOT_RECRUITING') GROUP BY phase;",
    "overdue_trials": "SELECT nct_id, title, completion_date, status FROM trials WHERE completion_date < date('now') AND status NOT IN ('COMPLETED','TERMINATED');",
    "top_conditions": "SELECT condition, COUNT(*) as trial_count FROM trials WHERE status IN ('RECRUITING','ACTIVE_NOT_RECRUITING') GROUP BY condition ORDER BY trial_count DESC LIMIT 10;"
}

def run_query(name):
    conn = sqlite3.connect("az_trials.db")
    cursor = conn.execute(QUERIES[name])
    results = cursor.fetchall()
    conn.close()
    return results

def ask_agent(user_question):
    routing_prompt = f"""A user asked: "{user_question}"
Which of these queries best answers it? Reply with ONLY the key name, nothing else.
- trials_by_phase: counts of active trials grouped by phase
- overdue_trials: trials past their completion date but not marked done
- top_conditions: conditions/therapeutic areas with the most active trials
"""
    routing_response = model.generate_content(routing_prompt)
    query_key = routing_response.text.strip()

    results = run_query(query_key)

    explain_prompt = f"""The user asked: "{user_question}"
The raw query results are: {results}
Answer their question in 2-3 plain sentences, using these results."""
    final_response = model.generate_content(explain_prompt)
    return final_response.text

if __name__ == "__main__":
    question = input("Ask about AstraZeneca's trials: ")
    print(ask_agent(question))