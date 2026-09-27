---
name: slack
description: Expert Slack platform assistance covering Bolt SDK (JavaScript/Python), Block Kit visual interfaces, slash commands, incoming webhooks, and enterprise app distribution. Use when building Slack bots, designing interactive Block Kit messages, processing Slack events, or managing workspace automations.
---

# Slack

Slack is the OS of work. 2025 turns it into an **Agentic OS** where AI agents can read messages, summarize threads, and trigger workflow actions autonomously.

## When to Use

- **ChatOps & Incident Management**: Building bots to trigger deployments, scale Kubernetes pods, and declare incident war rooms.
- **Automated Workflow Notifications**: Dispatching rich interactive alerts from CI/CD pipelines, PagerDuty, and cloud monitoring.
- **Interactive Engineering Workflows**: Creating modal dialogs, approval buttons, and slash commands using Slack Bolt SDK.
- **Team Collaboration & Knowledge Triage**: Searching message histories, archiving technical decisions, and managing channels.

## Quick Start

### 1. Minimal Bolt App (Node.js)

```javascript
import { App } from "@slack/bolt";

const app = new App({
  token: process.env.SLACK_BOT_TOKEN,
  signingSecret: process.env.SLACK_SIGNING_SECRET,
  socketMode: true,
  appToken: process.env.SLACK_APP_TOKEN,
});

app.command("/deploy", async ({ command, ack, respond }) => {
  await ack();
  await respond({
    text: `🚀 Initiated deploy for ${command.text}!`,
  });
});

(async () => {
  await app.start(process.env.PORT || 3000);
  console.log("⚡️ Bolt app is running!");
})();
```

### 2. Install Bolt

```bash
npm install @slack/bolt
```

## Core Concepts

### Modern Slack Bot with Bolt SDK for JavaScript

Creating an interactive Slack app handling slash commands, button clicks, and modal submissions:

```typescript
import { App, LogLevel } from "@slack/bolt";

const app = new App({
  token: process.env.SLACK_BOT_TOKEN,
  signingSecret: process.env.SLACK_SIGNING_SECRET,
  socketMode: true,
  appToken: process.env.SLACK_APP_TOKEN,
  logLevel: LogLevel.INFO,
});

// Handle /deploy slash command
app.command("/deploy", async ({ command, ack, client }) => {
  await ack();

  // Open an interactive modal dialog
  await client.views.open({
    trigger_id: command.trigger_id,
    view: {
      type: "modal",
      callback_id: "deploy_modal",
      title: { type: "plain_text", text: "Production Deployment" },
      submit: { type: "plain_text", text: "Deploy Now" },
      close: { type: "plain_text", text: "Cancel" },
      blocks: [
        {
          type: "input",
          block_id: "service_block",
          element: {
            type: "static_select",
            action_id: "service_select",
            placeholder: { type: "plain_text", text: "Select a microservice" },
            options: [
              {
                text: { type: "plain_text", text: "Auth Service" },
                value: "auth",
              },
              {
                text: { type: "plain_text", text: "Billing Service" },
                value: "billing",
              },
            ],
          },
          label: { type: "plain_text", text: "Target Service" },
        },
      ],
    },
  });
});

// Handle Modal Submission
app.view("deploy_modal", async ({ ack, body, view, client }) => {
  await ack();
  const selectedService =
    view.state.values.service_block.service_select.selected_option?.value;

  // Post confirmation message to incident channel
  await client.chat.postMessage({
    channel: process.env.SLACK_DEPLOY_CHANNEL_ID!,
    text: `:rocket: Deployment initiated for *${selectedService}* by <@${body.user.id}>`,
  });
});

(async () => {
  await app.start();
  console.log("⚡️ Slack Bolt app running in Socket Mode!");
})();
```

### Rich Block Kit Alerts for CI/CD Failure

Sending high-priority Block Kit notifications via Webhook:

```json
{
  "blocks": [
    {
      "type": "header",
      "text": {
        "type": "plain_text",
        "text": "🚨 Production Pipeline Build Failed",
        "emoji": true
      }
    },
    {
      "type": "section",
      "fields": [
        { "type": "mrkdwn", "text": "*Service:*\nPayments API" },
        { "type": "mrkdwn", "text": "*Environment:*\nProduction" },
        { "type": "mrkdwn", "text": "*Branch:*\n`main`" },
        { "type": "mrkdwn", "text": "*Triggered By:*\n`ci-runner-04`" }
      ]
    },
    {
      "type": "actions",
      "elements": [
        {
          "type": "button",
          "text": { "type": "plain_text", "text": "View Build Logs" },
          "url": "https://ci.example.com/build/12345",
          "style": "danger"
        }
      ]
    }
  ]
}
```

## Common Patterns

### Interactive Block Kit Message with Action Handler

**Problem**: Send structured notifications with interactive buttons and handle user clicks.  
**Solution**: Construct Block Kit JSON and bind action listeners in Bolt.

```javascript
// Post message with action button
await app.client.chat.postMessage({
  channel: "C12345678",
  blocks: [
    {
      type: "section",
      text: { type: "mrkdwn", text: "*Production Alert*: High CPU detected." },
    },
    {
      type: "actions",
      elements: [
        {
          type: "button",
          text: { type: "plain_text", text: "Acknowledge" },
          style: "primary",
          action_id: "ack_alert_button",
          value: "alert_42",
        },
      ],
    },
  ],
});

// Handle button interaction
app.action("ack_alert_button", async ({ body, ack, say }) => {
  await ack();
  await say(`<@${body.user.id}> acknowledged the incident!`);
});
```

### Incoming Webhook Simple Alert

**Problem**: Send quick status alerts from CI/CD pipeline without full bot setup.  
**Solution**: POST JSON payload to webhook URL.

```bash
curl -X POST -H 'Content-type: application/json' \
  --data '{"text":"Build #415 passed successfully on main."}' \
  "$SLACK_WEBHOOK_URL"
```

## Best Practices (2026)

- **Do** use **Socket Mode** for internal enterprise bots to eliminate the need for exposing public webhook ingress URLs.
- **Do** acknowledge events and commands within 3 seconds (`await ack()`) to prevent Slack API timeouts.
- **Do** construct structured messages using **Block Kit Builder** rather than legacy plaintext formatting.
- **Do** store bot tokens (`xoxb-`) and signing secrets in encrypted secret managers (AWS SSM, Vault).
- **Don't** broadcast unaggregated alerts to `@channel` or `@here` for non-critical, informational events.
- **Don't** log sensitive customer data or authorization credentials in Slack message channels.
- **Don't** run long synchronous background jobs inside the initial command handler; delegate to background workers.

## Troubleshooting

| Error / Symptom                                         | Cause                                               | Solution                                                                                             |
| ------------------------------------------------------- | --------------------------------------------------- | ---------------------------------------------------------------------------------------------------- |
| `dispatch_failed` when running slash command            | App took longer than 3,000ms to acknowledge request | Call `await ack()` immediately before executing asynchronous long-running tasks.                     |
| `invalid_auth`                                          | Invalid bot token or scopes missing                 | Verify bot token starts with `xoxb-` and requested scopes (`chat:write`, `commands`) are authorized. |
| Interactive buttons do nothing / show exclamation error | Request URL not configured in Slack App dashboard   | Under **Interactivity & Shortcuts**, enable Interactivity and set Request URL or use Socket Mode.    |

## References

- [Slack API](https://api.slack.com/)
