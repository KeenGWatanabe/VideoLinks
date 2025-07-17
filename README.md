Here's a **step-by-step guide** to creating and deploying your Azure Function App from **Visual Studio Code**, using a **Timer Trigger**, **Microsoft Graph API**, and **SendGrid** for email delivery.

---a

## 🧰 Prerequisites
Make sure you have:
- ✅ [Azure Functions extension for VS Code](https://learn.microsoft.com/en-us/azure/azure-functions/functions-develop-vs-code)
- ✅ Azure CLI installed
- ✅ Azure Functions Core Tools
- ✅ A registered Azure AD App with permissions for Microsoft Graph
- ✅ A SendGrid account and API key (or use Azure Communication Services)

---

## 🛠️ Step-by-Step Setup

### 1. **Create the Azure Function Project**
```bash
func init VideoEmailFunction --worker-runtime dotnet
cd VideoEmailFunction
func new --name SendVideoEmail --template "Timer trigger"
```
Choose a CRON expression like `0 0 9 * * *` for 9 AM daily.

---

### 2. **Add Microsoft Graph SDK**
In `VideoEmailFunction.csproj`, add:
```xml
<PackageReference Include="Microsoft.Graph" Version="5.0.0" />
<PackageReference Include="Microsoft.Identity.Client" Version="4.54.0" />
```

Run:
```bash
dotnet restore
```

---

### 3. **Authenticate with Microsoft Graph**
Use **client credentials flow**:
```csharp
var confidentialClient = ConfidentialClientApplicationBuilder
    .Create(clientId)
    .WithClientSecret(clientSecret)
    .WithTenantId(tenantId)
    .Build();

var authProvider = new ClientCredentialProvider(confidentialClient);
var graphClient = new GraphServiceClient(authProvider);
```

---

### 4. **Query SharePoint List**
Use Graph API to get items from your `VideoEmailTriggers` list:
```csharp
var items = await graphClient
    .Sites["sascosg.sharepoint.com"]
    .Lists["VideoEmailTriggers"]
    .Items
    .Request()
    .GetAsync();
```

---

### 5. **Send Email via SendGrid**
Install SendGrid SDK:
```bash
dotnet add package SendGrid
```

Send email:
```csharp
var client = new SendGridClient(sendGridApiKey);
var from = new EmailAddress("your@email.com", "IT Team");
var subject = "Your Scheduled Video";
var to = new EmailAddress(userEmail);
var plainTextContent = "Here's your video: " + videoUrl;
var msg = MailHelper.CreateSingleEmail(from, to, subject, plainTextContent, null);
await client.SendEmailAsync(msg);
```

---

### 6. **Deploy to Azure**
```bash
func azure functionapp publish <YourFunctionAppName>
```

---

## 🧠 Tips
- Store secrets in `local.settings.json` for local dev.
- Use Azure Key Vault or App Settings for production secrets.
- Use `DateTime.UtcNow - StartDate` to determine which video to send.

---

Want me to help scaffold the full function code or set up the app registration for Graph API?