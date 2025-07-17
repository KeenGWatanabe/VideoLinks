from msal import PublicClientApplication
import requests, pandas as pd
import os

print("🚀 Script started")

client_id = '193b1b22-bf91-4ea0-97c5-a7f695c66680'
tenant_id = '59f078e1-e31b-4c6f-a065-784102e9823d'
authority = f'https://login.microsoftonline.com/{tenant_id}'
scopes = ['User.Read.All', 'Reports.Read.All']

app = PublicClientApplication(client_id, authority=authority)

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

