# Bin Collection Reminder

A simple, containerized service that checks Vale of White Horse bin collection schedule and sends reminders through multiple notification channels.

## Features

- Retrieves bin collection information for Vale of White Horse Council
- Supports multiple notification methods:
  - Discord webhooks
  - WhatsApp (via CallMeBot)
  - Email
- Configurable schedule via cron
- Easy deployment with Docker and Docker Compose

## Quick Start

1. Clone this repository:
```bash
git clone https://github.com/yourusername/bin-collection-reminder.git
cd bin-collection-reminder
```

2. Edit `.env` with your UPRN and notification preferences:
```
# Required settings
UPRN=

# Cron settings (default: Monday at 6PM)
CRON_SCHEDULE=0 18 * * 1

# Discord notification settings
DISCORD_ENABLED=true
DISCORD_WEBHOOK=https://discord.com/api/webhooks/your-webhook-url

# WhatsApp (CallMeBot) notification settings
WHATSAPP_ENABLED=false
WHATSAPP_PHONE=+1234567890
WHATSAPP_APIKEY=your-api-key

# Email notification settings
EMAIL_ENABLED=false
EMAIL_SMTP_SERVER=smtp.gmail.com
EMAIL_SMTP_PORT=587
EMAIL_SENDER=your-email@gmail.com
EMAIL_PASSWORD=your-password
EMAIL_RECIPIENT=recipient@example.com
```

3. Build and start the container:
```bash
docker-compose up -d
```

## How It Works

The service fetches bin collection information from the Vale of White Horse Council website using your UPRN (Unique Property Reference Number). It extracts the next collection day and type, then sends notifications through your configured channels.

The container runs on a schedule defined by the `CRON_SCHEDULE` environment variable. By default, it runs every Monday at 6PM.

## Finding Your UPRN

You can find your UPRN (Unique Property Reference Number) by:
1. Visiting the [Vale of White Horse Council website](https://www.whitehorsedc.gov.uk/)
2. Searching for your property on their bin collection service
3. Look for a long number in the URL or page source, which is your UPRN

## Configuration Options

| Variable | Description | Default |
|----------|-------------|---------|
| UPRN | Your Unique Property Reference Number | (Required) |
| CRON_SCHEDULE | When to run the check (cron format) | 0 18 * * 1 |
| DISCORD_ENABLED | Enable Discord notifications | false |
| DISCORD_WEBHOOK | Discord webhook URL | |
| WHATSAPP_ENABLED | Enable WhatsApp notifications | false |
| WHATSAPP_PHONE | Your phone number with country code | |
| WHATSAPP_APIKEY | Your CallMeBot API key | |
| EMAIL_ENABLED | Enable email notifications | false |
| EMAIL_SMTP_SERVER | SMTP server address | smtp.gmail.com |
| EMAIL_SMTP_PORT | SMTP server port | 587 |
| EMAIL_SENDER | Sender email address | |
| EMAIL_PASSWORD | Sender email password or app password | |
| EMAIL_RECIPIENT | Recipient email address | |

## Project Structure

```
bin-collection-reminder/
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── scripts/
│   ├── bin_collection.py
│   └── notifications.py
├── entrypoint.sh
└── .env
```

## Requirements

- Docker
- Docker Compose
- Your personal UPRN

## CallMeBot Setup

To use WhatsApp notifications:

1. Visit [CallMeBot's WhatsApp page](https://www.callmebot.com/blog/free-api-whatsapp-messages/)
2. Follow their instructions to get your API key
3. Update your `.env` file with your phone number and API key

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Acknowledgments

- Based on UK bin collection data services
- Inspired by other notification services
