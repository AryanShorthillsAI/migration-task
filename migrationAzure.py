import requests
from requests.auth import HTTPBasicAuth
import time
from dotenv import load_dotenv
import os

load_dotenv()

SOURCE_PAT = os.getenv("SOURCE_PAT")
DEST_PAT = os.getenv("DEST_PAT")

SOURCE_ORG = "anand-test-org"
SOURCE_PROJECT = "anand-projectB"

DEST_ORG = "balraj-test-org"
DEST_PROJECT = "balraj-projectB"

HEADERS = {
    "Content-Type": "application/json-patch+json"
}

def get_auth(pat):
    return HTTPBasicAuth("", pat)

def get_work_items():
    url = f"https://dev.azure.com/{SOURCE_ORG}/{SOURCE_PROJECT}/_apis/wit/wiql?api-version=7.1"
    query = {
        "query": f"SELECT [System.Id] FROM WorkItems WHERE [System.TeamProject] = '{SOURCE_PROJECT}'"
    }
    resp = requests.post(url, json=query, auth=get_auth(SOURCE_PAT))
    resp.raise_for_status()
    ids = [item["id"] for item in resp.json()["workItems"]]
    print(f"🔍 Found {len(ids)} work items to migrate.")
    return ids

def get_work_item_details(wi_id):
    url = f"https://dev.azure.com/{SOURCE_ORG}/_apis/wit/workitems/{wi_id}?$expand=all&api-version=7.1"
    resp = requests.get(url, auth=get_auth(SOURCE_PAT))
    resp.raise_for_status()
    return resp.json()

def work_item_exists(title):
    url = f"https://dev.azure.com/{DEST_ORG}/{DEST_PROJECT}/_apis/wit/wiql?api-version=7.1"
    query = {
        "query": f"SELECT [System.Id] FROM WorkItems WHERE [System.Title] = '{title}'"
    }
    resp = requests.post(url, json=query, auth=get_auth(DEST_PAT))
    resp.raise_for_status()
    return bool(resp.json().get("workItems"))

def create_initial_work_item(title, tags, assigned_to):
    url = f"https://dev.azure.com/{DEST_ORG}/{DEST_PROJECT}/_apis/wit/workitems/$Task?api-version=7.1"
    payload = [
        {"op": "add", "path": "/fields/System.Title", "value": title}
    ]
    if tags:
        payload.append({"op": "add", "path": "/fields/System.Tags", "value": tags})
    if assigned_to:
        payload.append({"op": "add", "path": "/fields/System.AssignedTo", "value": assigned_to})
    resp = requests.post(url, headers=HEADERS, json=payload, auth=get_auth(DEST_PAT))
    resp.raise_for_status()
    return resp.json()["id"]

def update_work_item_fields(wi_id, state, description, fields,priority=None, activity=None, remaining_work=None):
    url = f"https://dev.azure.com/{DEST_ORG}/{DEST_PROJECT}/_apis/wit/workitems/{wi_id}?api-version=7.1"
    payload = []
    if state in {"To Do", "Doing", "In Progress"}:
        payload.append({"op": "add", "path": "/fields/System.State", "value": state})
    if description:
        payload.append({"op": "add", "path": "/fields/System.Description", "value": description})
    if priority is not None:
        payload.append({"op": "add", "path": "/fields/Microsoft.VSTS.Common.Priority", "value": priority})
    if activity:
        payload.append({"op": "add", "path": "/fields/Microsoft.VSTS.Common.Activity", "value": activity})
    if remaining_work is not None:
        payload.append({"op": "add", "path": "/fields/Microsoft.VSTS.Scheduling.RemainingWork", "value": remaining_work})

    # Custom fields
    custom_field_map = {
        "Custom.EffortHours": "Effort Hours",
        "Microsoft.VSTS.Scheduling.StartDate": "Start Date",
        "Microsoft.VSTS.Scheduling.DueDate": "Due Date",
        "Custom.RevisedDueDate": "Revised Due Date",
        "Custom.PlannedType": "Planned Type",
        "Custom.IntegratedinBuild": "Integrated in Build"
    }

    for api_field, readable_name in custom_field_map.items():
        value = fields.get(api_field)
        if value:
            payload.append({"op": "add", "path": f"/fields/{api_field}", "value": value})
    
    resp = requests.patch(url, headers=HEADERS, json=payload, auth=get_auth(DEST_PAT))
    resp.raise_for_status()

def migrate_comments(source_id, dest_id):
    # GET comments using 7.1-preview.4
    get_url = f"https://dev.azure.com/{SOURCE_ORG}/{SOURCE_PROJECT}/_apis/wit/workItems/{source_id}/comments?api-version=7.1-preview.4"
    resp = requests.get(get_url, auth=get_auth(SOURCE_PAT))

    if resp.status_code != 200:
        print(f"❌ Failed to fetch comments for work item {source_id}")
        print(f"Status Code: {resp.status_code}")
        print(f"Response: {resp.text}")
        return

    comments = resp.json().get("comments", [])
    for comment in comments:
        post_url = f"https://dev.azure.com/{DEST_ORG}/{DEST_PROJECT}/_apis/wit/workItems/{dest_id}/comments?api-version=7.0-preview.3"
        data = {"text": comment["text"]}
        post_resp = requests.post(post_url, json=data, auth=get_auth(DEST_PAT))
        if post_resp.status_code >= 300:
            print(f"❌ Failed to post comment to work item {dest_id}: {post_resp.status_code} - {post_resp.text}")

def migrate_all():
    for wi_id in get_work_items():
        try:
            wi = get_work_item_details(wi_id)
            title = wi["fields"]["System.Title"]
            state = wi["fields"].get("System.State", "To Do")
            description = wi["fields"].get("System.Description", "")
            priority = wi["fields"].get("Microsoft.VSTS.Common.Priority")
            activity = wi["fields"].get("Microsoft.VSTS.Common.Activity")
            remaining_work = wi["fields"].get("Microsoft.VSTS.Scheduling.RemainingWork")
            assigned_to = wi["fields"].get("System.AssignedTo", {}).get("displayName")
            tags = wi["fields"].get("System.Tags", "")

            if work_item_exists(title):
                print(f"⚠️ Skipping duplicate: {title}")
                continue

            new_id = create_initial_work_item(title, tags, assigned_to)
            time.sleep(1)  # Give Azure time to save the new item
            update_work_item_fields(new_id, state, description, wi["fields"], priority, activity, remaining_work)
            migrate_comments(wi_id, new_id)
            print(f"✅ Migrated work item {wi_id} → {new_id}")

        except Exception as e:
            print(f"❌ Failed to create work item: {e}")

    print("🎉 Migration complete.")

if __name__ == "__main__":
    migrate_all()
    
