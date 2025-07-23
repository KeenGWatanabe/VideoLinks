load_dotenv() # Loads .env into os.environ

import os
import json
import requests
import azure.functions as func
from sendgrid import SendGridAPIClient
from shareplum import Site, Office365
from azure.identity import DefaultAzureCredential
from office365.runtime.auth.client_credential import ClientCredential
from office365.sharepoint.client_context import ClientContext
from dotenv import load_dotenv


# Credentials Variables
client_id = os.getenv("AZURE_CLIENT_ID")
tenant_id = os.getenv("AZURE_TENANT_ID")
client_secret = os.getenv("AZURE_CLIENT_SECRET")
site_url = "https://sascosg.sharepoint.com/sites/VideoLinks"

# Create SharePoint client with proper credentials
credentials = ClientCredential(client_id, client_secret)
ctx = ClientContext(site_url).with_credentials(credentials)

# function call
app = func.FunctionApp()

@app.function_name(name="SendVideoEmails")
@app.route(route="SendVideoEmails", auth_level=func.AuthLevel.ANONYMOUS)
def main(req: func.HttpRequest) -> func.HttpResponse:
    try:
        # Your function logic here
        return func.HttpResponse("Email sending function triggered!")
    except Exception as e:
        return func.HttpResponse(f"Error: {str(e)}", status_code=500)

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