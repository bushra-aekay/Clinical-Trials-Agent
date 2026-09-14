import requests
import pandas as pd

url = "https://clinicaltrials.gov/api/v2/studies"
params = {
    "query.spons": "AstraZeneca",
    "pageSize": 200,
    "fields": "NCTId,BriefTitle,OverallStatus,Phase,Condition,EnrollmentCount,StartDate,CompletionDate"
}

response = requests.get(url, params=params)
data = response.json()

rows = []
for study in data.get("studies", []):
    s = study["protocolSection"]
    rows.append({
        "nct_id": s["identificationModule"].get("nctId"),
        "title": s["identificationModule"].get("briefTitle"),
        "status": s["statusModule"].get("overallStatus"),
        "phase": ", ".join(s.get("designModule", {}).get("phases", [])),
        "condition": ", ".join(s.get("conditionsModule", {}).get("conditions", [])),
        "enrollment": s.get("designModule", {}).get("enrollmentInfo", {}).get("count"),
        "start_date": s["statusModule"].get("startDateStruct", {}).get("date"),
        "completion_date": s["statusModule"].get("completionDateStruct", {}).get("date"),
    })

df = pd.DataFrame(rows)
df.to_csv("az_trials.csv", index=False)
print(f"Pulled {len(df)} trials.")