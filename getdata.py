import requests
import json
import pandas as pd
import os
from dotenv import load_dotenv


JIRA_URL = F"https://{os.getenv('JIRA_HOST')}/rest/api/3/search"
AUTH = (os.getenv('JIRA_USER_ID'), os.getenv('JIRA_API_TOKEN'))
MAX_PAGES = 5

params = {
    "jql": "project = BUPL",
    "maxResults": 100,
    "startAt": 0,
    "fields": "summary,issuetype,status,priority,assignee,reporter,created,updated"
}

all_issues = []


current_page = 0

while True:
    response = requests.get(JIRA_URL, auth=AUTH, params=params)
    data = response.json()
    
    if "issues" not in data or not data["issues"]:
        break  # Stop if no more issues are returned
    
    all_issues.extend(data["issues"])  # Append new issues

    params["startAt"] += params["maxResults"]  # Move to next page
    
    current_page += 1
    if current_page >= MAX_PAGES:
        break  # Stop if max pages reached

df = pd.json_normalize(all_issues)
df.to_csv("jira_data.csv", index=False)

print(f"Retrieved {len(all_issues)} issues for the BUPL project and saved to jira_data.csv")
