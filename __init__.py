import os
import json
import requests
from sendgrid import SendGridAPIClient
from shareplum import Site, Office365
from azure.identity import DefaultAzureCredential
from office365.sharepoint.client_context import ClientContext
from dotenv import load_dotenv

load_dotenv() # Loads .env into os.environ

# Use environment variables (NEVER hardcode secrets!)
client_id = os.environ['AZURE_CLIENT_ID']
tenant_id = os.environ['AZURE_TENANT_ID']
credential = DefaultAzureCredential() 



# Connect to SharePoint
ctx = ClientContext("https://sascosg.sharepoint.com/sites/VideoLinks").with_credentials(credential)

def main(req):
    # Example: Get subscribers from the list
    subscribers = ctx.web.lists.get_by_title("VideoSubscribers").items.get().execute_query()
    return {
        "body": f"Found {len(subscribers)} subscribers."
    }

    # Get subscribers
    subscribers = requests.get(
        "https://sascosg.sharepoint.com/sites/VideoLinks/_api/web/lists/getbytitle('VideoSubscribers')/items",
        cookies=authcookie
    ).json()

    # Get videos
    videos = [
        "https://sascosg.sharepoint.com/sites/ITTeam/_layouts/15/stream.aspx[...]AddSafeEmails.mp4",
        "https://sascosg.sharepoint.com/sites/ITTeam/_layouts/15/stream.aspx[...]SetupSharepoint.mp4"
    ]

    # Send emails
    for user in subscribers:
        message = {
            "personalizations": [{
                "to": [{"email": user['Email']}],
                "subject": "Your Video Links"
            }],
            "content": [{
                "type": "text/html",
                "value": f"Videos:<br>1. <a href='{videos[0]}'>Add Safe Emails</a><br>2. <a href='{videos[1]}'>SharePoint Setup</a>"
            }]
        }
        SendGridAPIClient(os.environ['SENDGRID_KEY']).send(message)

    return func.HttpResponse("Emails sent!")