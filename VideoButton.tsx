// VideoButton.tsx
export const VideoButton = () => {
  const triggerEmails = async () => {
    await fetch("https://your-function.azurewebsites.net/api/sendVideoEmails", {
      method: "POST",
      headers: { "Content-Type": "application/json" }
    });
    alert("Emails queued!");
  };

  return <button onClick={triggerEmails}>Send Videos</button>;
};