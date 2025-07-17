from msal import PublicClientApplication
import requests, pandas as pd
import os

print("🚀 Script started")

client_id = os.environ["AZURE_CLIENT_ID"]  # Changed from hardcoded
tenant_id = os.environ["AZURE_TENANT_ID"]  # Changed from hardcoded
authority = f'https://login.microsoftonline.com/{tenant_id}'
scopes = ['User.Read.All', 'Reports.Read.All']

# Initialize MSAL client
app = PublicClientApplication(client_id, authority=authority)

print(f"✅ Config loaded - Client ID: {client_id}, Tenant: {tenant_id}")


# 🔐 Use device code flow for WSL/fixed-terminal authentication
flow = app.initiate_device_flow(scopes=scopes)
if 'user_code' not in flow:
    raise ValueError("Device flow initiation failed. Response: %s" % flow)

print(f"\n👉 Please go to {flow['verification_uri']} and enter the code: {flow['user_code']}\n")
result = app.acquire_token_by_device_flow(flow)

if 'access_token' in result:
    print("✅ Authenticated successfully")
    headers = {'Authorization': f"Bearer {result['access_token']}"}
    graph_url = 'https://graph.microsoft.com/v1.0/users?$select=displayName,userPrincipalName,jobTitle'
    users = requests.get(graph_url, headers=headers).json()

    print("👥 Users fetched:", len(users.get("value", [])))

    df = pd.DataFrame(users['value'])
    output_path = os.path.join(os.getcwd(), 'm365_users.csv')
    df.to_csv(output_path, index=False)

    print(f"📄 Report saved to: {output_path}")
else:
    print("❌ Authentication failed")

