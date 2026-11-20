# Scene Sandbox: Google Drive edition

The Scene Sandbox, running as a Google Apps Script web app that lives in your own Google Drive. You open it from a link
(bookmark it, or add it to your phone's home screen). Live scenes come from Claude through the Anthropic API, using your
own API key.

**Files**
- `Code.gs`: the server side. It holds no secrets; it reads your key from the project's settings and calls Claude.
- `Index.html`: the page itself, with all the character art built in.

## What you need

- A Google account.
- An Anthropic API key from https://console.anthropic.com (API keys). The API is billed separately from a Claude.ai
  subscription: you add credit in the Console. A scene beat typically costs a few cents.

## Setup (about five minutes, once)

1. **Create the project in Drive.** In Google Drive: New > More > Google Apps Script. Rename it "Scene Sandbox".
2. **Add the server code.** In the editor, open `Code.gs`, delete what's there, and paste in the contents of `Code.gs`.
3. **Add the page.** Click + next to Files > HTML, name it exactly `Index` (the editor adds `.html`), delete what's
   there, and paste in the contents of `Index.html`. Save (Ctrl/Cmd+S).
4. **Add your API key privately.** Project Settings (the gear) > Script properties > Add script property.
   Property: `ANTHROPIC_API_KEY`. Value: your key. Save. The key stays in the project's settings and never reaches the
   page or anyone who opens it.
5. **Deploy it.** Deploy > New deployment > the gear next to "Select type" > Web app.
   - Execute as: **Me**
   - Who has access: **Only myself**
   Click Deploy, then Authorize access and allow it (Google asks because the script connects to an outside service:
   the Anthropic API). If Google warns that the app isn't verified, choose Advanced > Go to Scene Sandbox: it's your
   own script.
6. **Open it.** Copy the Web app URL and open it. Bookmark it, or on a phone use Add to Home Screen.

## Updating later

Paste the new file contents in, then Deploy > Manage deployments > the pencil icon > Version: New version > Deploy.
The link stays the same.

## Good to know

- Scenes appear a beat at a time instead of streaming word by word (Apps Script waits for each full answer).
- Read aloud uses your device's built-in voices.
- Saved scenes are kept in the browser you use, not in Drive.
- With "Only myself", nobody else can open the link. To share it, change "Who has access", but every scene they run
  is billed to your API key.
- If a beat ever takes too long and fails, press "Try that beat again"; Apps Script limits how long one request can run.
