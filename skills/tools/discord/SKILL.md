---
name: discord
description: Expert Discord API and bot development assistance covering Discord.js, slash commands, gateway intents, webhooks, and embeds. Use when building interactive Discord bots and notification integrations.
---

# Discord

Discord is where developer communities live. 2025 updates to the **Social SDK** allow building rich "Activities" (Embedded Apps) inside Discord.

## When to Use

- **Developer Community & Team Collaboration**: Real-time voice, video, text chat, and automated notification channels.
- **Automated DevOps & CI/CD Webhooks**: Posting build statuses, deployment alerts, and incident notifications to channels.
- **Interactive Bot & Slash Command Development**: Building Discord applications with `discord.js` or `discord.py`.
- **Engineering Support & Incident War Rooms**: Coordinating outage responses with integrated monitoring bots.

## Quick Start

```javascript
import { Client, GatewayIntentBits } from "discord.js";

const client = new Client({ intents: [GatewayIntentBits.Guilds] });

client.on("ready", () => {
  console.log(`Bot logged in as ${client.user.tag}!`);
});

client.on("interactionCreate", async (interaction) => {
  if (!interaction.isChatInputCommand()) return;
  if (interaction.commandName === "ping") {
    await interaction.reply("Pong!");
  }
});

client.login(process.env.DISCORD_TOKEN);
```

## Core Concepts

#Sending Automated Alerts via Incoming Webhook

Posting formatted embed messages from CI/CD pipelines using curl:

```bash
# Post structured deployment notification to Discord channel
curl -X POST \
  -H "Content-Type: application/json" \
  -d '{
    "username": "Deployment Bot",
    "embeds": [
      {
        "title": "Production Deployment Succeeded",
        "description": "API service v2026.1.0 deployed to all edge regions.",
        "color": 65280,
        "fields": [
          {"name": "Commit", "value": "a1b2c3d", "inline": true},
          {"name": "Author", "value": "devops-team", "inline": true}
        ],
        "footer": {"text": "Antigravity CI/CD Pipeline"}
      }
    ]
  }' "$DISCORD_WEBHOOK_URL"
```

#Discord Bot with Slash Commands (discord.py)

Building an interactive moderation or query bot:

```python
import os
import discord
from discord import app_commands

intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

@tree.command(name="status", description="Query current infrastructure status")
async def status_command(interaction: discord.Interaction):
    await interaction.response.send_message("All systems operational. API latency: 24ms.", ephemeral=True)

@client.event
async def on_ready():
    await tree.sync()
    print(f"Logged in as {client.user} (Slash commands synchronized)")

# client.run(os.environ["DISCORD_BOT_TOKEN"])
```

#Interactive Buttons & Select Menus (discord.js)

Handling UI component interactions:

```javascript
import {
  Client,
  GatewayIntentBits,
  ButtonBuilder,
  ButtonStyle,
  ActionRowBuilder,
} from "discord.js";

const client = new Client({ intents: [GatewayIntentBits.Guilds] });

client.on("interactionCreate", async (interaction) => {
  if (
    interaction.isChatInputCommand() &&
    interaction.commandName === "deploy"
  ) {
    const confirm = new ButtonBuilder()
      .setCustomId("confirm_deploy")
      .setLabel("Confirm Production Release")
      .setStyle(ButtonStyle.Danger);

    const row = new ActionRowBuilder().addComponents(confirm);
    await interaction.reply({
      content: "Are you sure you want to deploy to production?",
      components: [row],
    });
  }
});
```

## Common Patterns

### Webhook Notification Delivery with Rich Embeds

**Problem**: Sending automated build or deployment notifications to Discord without running a persistent bot.

**Solution**:
Post directly to incoming Discord Webhook:

```javascript
async function sendDeployAlert(webhookUrl, deployInfo) {
  await fetch(webhookUrl, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      embeds: [
        {
          title: "🚀 Deployment Successful",
          color: 0x10b981,
          fields: [
            { name: "Environment", value: deployInfo.env, inline: true },
            { name: "Commit", value: deployInfo.commitHash, inline: true },
          ],
          timestamp: new Date().toISOString(),
        },
      ],
    }),
  });
}
```

## Best Practices (2026)

- **Do** store Discord bot tokens and webhook URLs in secure environment variables, never in code.
- **Do** use modern Application Slash Commands (`/command`) rather than legacy message prefix commands (`!command`).
- **Do** set `ephemeral=True` for sensitive bot responses so they are visible only to the invoking user.
- **Do** specify only the exact Gateway Intents required by the bot to minimize memory and bandwidth.
- **Don't** expose webhook URLs publicly; anyone with the URL can post arbitrary messages to the channel.
- **Don't** block the async event loop in bots; offload heavy computations or I/O with threads or queues.
- **Don't** spam channels with noisy alert webhooks; aggregate and summarize notifications.

## Troubleshooting

| Error                                            | Cause                                                                                 | Solution                                                                 |
| :----------------------------------------------- | :------------------------------------------------------------------------------------ | :----------------------------------------------------------------------- |
| `Disallowed Intent: Privileged intent requested` | Bot requests `MessageContent` or `GuildMembers` without enabling in Developer Portal. | Enable Privileged Gateway Intents in Discord Developer Portal > Bot tab. |
| `DiscordAPIError[10062]: Unknown interaction`    | Bot took longer than 3 seconds to reply without deferring.                            | Acknowledge immediately: `await interaction.deferReply()`.               |
| `Invalid token provided`                         | `DISCORD_TOKEN` contains whitespace, quotes, or revoked token.                        | Regenerate token in Developer Portal and set clean env var.              |

## References

- [Discord Developer Portal](https://discord.com/developers/docs/intro)
