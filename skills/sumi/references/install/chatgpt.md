# ChatGPT and browser-based assistants

A chat model and the app running it are different things. First ask: “Can you read this extracted folder, run Python/Node/FFmpeg here and return a real MP4?” A useful answer names actual available tools; a model name alone is not a capability check.

For ChatGPT desktop with local Work/Codex capabilities:

1. Extract the Beyondsumi ZIP and open/select that local folder in the desktop app.
2. Follow [the local Codex skills route](codex.md), or ask the assistant to read `skills/sumi/SKILL.md` directly from the shared folder.
3. Paste the [first-use request](../beginner-use.md). Check that the assistant actually reads the skill and reports its available tools.
4. If it cannot access the folder or render with the required tools, use a capable local agent for production. Chat can still help develop the story, script and direction.

A browser ChatGPT Project does not automatically provide access to your laptop's folders. Uploading a ZIP also does not guarantee Node/FFmpeg/image tools, persistent storage or a local dashboard. Use supported workspace skill/plugin import when available, then repeat the capability check; do not invent an “Install” button or assume an account feature exists.

For Claude web/Cowork, use the account's supported custom-skill upload/enable flow, one skill folder per supported upload. It is different from Claude Code's local `~/.claude/skills/` directory. Check current account controls and file/execution limits before uploading a large sound bank. The guide does not certify account-level uploads.

Sources: [OpenAI skills](https://learn.chatgpt.com/docs/build-skills), [local versus ChatGPT projects](https://learn.chatgpt.com/docs/projects), [Claude local/cloud skill loading](https://code.claude.com/docs/en/skills).
