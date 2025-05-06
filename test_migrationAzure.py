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
            
def migrate_attachments(source_id, dest_id):
    # Get work item details to find attachments
    source_url = f"https://dev.azure.com/{SOURCE_ORG}/_apis/wit/workitems/{source_id}?$expand=relations&api-version=7.1"
    resp = requests.get(source_url, auth=get_auth(SOURCE_PAT))
    resp.raise_for_status()

    work_item = resp.json()
    relations = work_item.get("relations", [])

    # Filter only attachments
    attachments = [rel for rel in relations if rel["rel"] == "AttachedFile"]

    print(f"📎 Found {len(attachments)} attachments for work item {source_id}")

    for attachment in attachments:
        attachment_url = attachment["url"]
        file_attributes = attachment.get("attributes", {})
        file_name = attachment.get("attributes", {}).get("name", "attachment")

        # Step 1: Download the attachment
        download_resp = requests.get(attachment_url, headers={"Accept": "application/octet-stream"}, auth=get_auth(SOURCE_PAT))
        if download_resp.status_code != 200:
            print(f"❌ Failed to download attachment {file_name} from work item {source_id}")
            continue

        file_content = download_resp.content

        # Step 2: Upload attachment to destination project
        upload_url = f"https://dev.azure.com/{DEST_ORG}/{DEST_PROJECT}/_apis/wit/attachments?fileName={file_name}&api-version=7.1"
        upload_resp = requests.post(upload_url, headers={"Content-Type": "application/octet-stream"}, data=file_content, auth=get_auth(DEST_PAT))
        if upload_resp.status_code >= 300:
            print(f"❌ Failed to upload attachment {file_name} to destination")
            continue

        attachment_reference_url = upload_resp.json()["url"]

        # Step 3: Link the uploaded attachment to the destination work item
        link_payload = [
            {
                "op": "add",
                "path": "/relations/-",
                "value": {
                    "rel": "AttachedFile",
                    "url": attachment_reference_url,
                    "attributes":file_attributes
                }
            }
        ]

        patch_url = f"https://dev.azure.com/{DEST_ORG}/{DEST_PROJECT}/_apis/wit/workitems/{dest_id}?api-version=7.1"
        patch_resp = requests.patch(patch_url, headers=HEADERS, json=link_payload, auth=get_auth(DEST_PAT))
        if patch_resp.status_code >= 300:
            print(f"❌ Failed to link attachment {file_name} to destination work item {dest_id}")
        else:
            print(f"✅ Migrated attachment {file_name} to work item {dest_id}")

def migrate_links(source_id, dest_id, id_mapping):
    """
    Migrates links (relations) from a source work item to its corresponding destination work item.
    Only links that also exist in id_mapping are recreated using their mapped destination IDs.
    """
    print("Start migrating links...")
    source_url = f"https://dev.azure.com/{SOURCE_ORG}/_apis/wit/workitems/{source_id}?$expand=relations&api-version=7.1"
    resp = requests.get(source_url, auth=get_auth(SOURCE_PAT))
    resp.raise_for_status()
    print("Link fetched")
    work_item = resp.json()
    relations = work_item.get("relations", [])
    
    migrated_links = []

    for relation in relations:
        rel_type = relation["rel"]
        url = relation["url"]

        # Skip attachments and external links
        if rel_type == "AttachedFile":
            continue

        # Extract source linked work item ID from URL
        try:
            print(type(url))
            linked_source_id = int(url.split("/")[-1])
            print(f"🔗 Found link to source work item {linked_source_id}")
        except ValueError:
            print(f"❌ Invalid link URL: {url}")
            continue

        # Only migrate if the linked source work item was migrated
        linked_dest_id = id_mapping.get(linked_source_id)
        
        if not linked_dest_id:
            print(f"⏭️ Skipping link to unmigrated work item {linked_source_id}")
            continue

        # Construct new destination URL
        dest_url = f"https://dev.azure.com/{DEST_ORG}/_apis/wit/workItems/{linked_dest_id}"
        link_payload = [{
            "op": "add",
            "path": "/relations/-",
            "value": {
                "rel": rel_type,
                "url": dest_url,
                "attributes": relation.get("attributes", {})
            }
        }]

        # Patch destination work item to add the relation
        patch_url = f"https://dev.azure.com/{DEST_ORG}/{DEST_PROJECT}/_apis/wit/workitems/{dest_id}?api-version=7.1"
        patch_resp = requests.patch(patch_url, headers=HEADERS, json=link_payload, auth=get_auth(DEST_PAT))

        if patch_resp.status_code < 300:
            print(f"🔗 Linked work item {dest_id} ↔ {linked_dest_id}")
            migrated_links.append(linked_dest_id)
        else:
            print(f"❌ Failed to link work item {dest_id} to {linked_dest_id}: {patch_resp.status_code} - {patch_resp.text}")

    if not migrated_links:
        print(f"ℹ️ No valid links migrated for work item {source_id}")


def migrate_and_get_id_mapping():
    """
    Migrates work items from source to destination and returns a mapping
    of source work item IDs to their corresponding destination IDs.
    Also maps already existing work items in destination.
    """
    id_mapping = {}

    for source_id in get_work_items():
        try:
            wi = get_work_item_details(source_id)
            title = wi["fields"]["System.Title"]
            state = wi["fields"].get("System.State", "To Do")
            description = wi["fields"].get("System.Description", "")
            assigned_to = wi["fields"].get("System.AssignedTo", {}).get("displayName")
            tags = wi["fields"].get("System.Tags", "")

            # Check if work item already exists in destination
            existing_id = find_existing_work_item_by_title(title)

            if existing_id:
                print(f"⚠️ Work item '{title}' already exists. Mapping source {source_id} → existing {existing_id}")
                id_mapping[source_id] = existing_id
                continue

            # # Create new destination work item
            # dest_id = create_initial_work_item(title, tags, assigned_to)
            # id_mapping[source_id] = dest_id

            # time.sleep(1)  # Give time for Azure DevOps to save
            # update_work_item_fields(dest_id, state, description)
            # migrate_comments(source_id, dest_id)

            # print(f"✅ Migrated work item {source_id} → {dest_id}")

        except Exception as e:
            print(f"❌ Failed to migrate work item {source_id}: {e}")

    print("🎉 Migration + Mapping complete.")
    return id_mapping

def find_existing_work_item_by_title(title):
    """
    Searches destination project for a work item by title.
    Returns the destination work item ID if found, else None.
    """
    url = f"https://dev.azure.com/{DEST_ORG}/{DEST_PROJECT}/_apis/wit/wiql?api-version=7.1"
    query = {
        "query": f"SELECT [System.Id] FROM WorkItems WHERE [System.Title] = '{title}'"
    }
    resp = requests.post(url, json=query, auth=get_auth(DEST_PAT))
    resp.raise_for_status()
    
    work_items = resp.json().get("workItems", [])
    if work_items:
        return work_items[0]["id"]
    return None


def migrate_all(id_mapping):
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
            migrate_attachments(wi_id, new_id)
            print(f"✅ Migrated work item {wi_id} → {new_id}")
            id_mapping[wi_id] = new_id
        
            migrate_links(wi_id, new_id,id_mapping)
            print(f"✅ Migrated links for work item {wi_id} → {new_id}")
            
        except Exception as e:
            print(f"❌ Failed to create work item: {e}")

    print("🎉 Migration complete.")

if __name__ == "__main__":
    id_mapping= migrate_and_get_id_mapping()
    print(id_mapping)
    migrate_all(id_mapping)
