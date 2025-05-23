# Bin Collection Reminder

A robust, containerized service that checks Vale of White Horse bin collection schedule and sends reminders through multiple notification channels.

## Features

- **Web Scraping**: Retrieves bin collection information from Vale of White Horse Council website using UPRN
- **Multi-Channel Notifications**: Supports Discord webhooks, WhatsApp (via CallMeBot), and Email
- **Scheduled Execution**: Configurable cron-based scheduling with Docker container
- **Containerized Deployment**: Easy deployment with Docker and Docker Compose

## Architecture Overview

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Docker        │    │  Cron Scheduler  │    │  Python Scripts│
│   Container     │───▶│  (configurable)  │───▶│                 │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                                                         │
                                                         ▼
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│  Vale of White  │◀───│  Web Scraper     │    │  Notification   │
│  Horse Council  │    │  (BeautifulSoup) │    │  Services       │
│  Website        │    └──────────────────┘    └─────────────────┘
└─────────────────┘                                     │
                                                         ▼
                                            ┌─────────────────┐
                                            │ Discord/WhatsApp│
                                            │ /Email Delivery │
                                            └─────────────────┘
```

## Quick Start

1. **Clone the repository**:

```bash
git clone https://github.com/yourusername/bin-collection-reminder.git
cd bin-collection-reminder
```

2. **Configure environment variables**:

```bash
cp env.template .env
# Edit .env with your settings (see Configuration section below)
```

3. **Deploy with Docker**:

```bash
docker-compose up -d
```

4. **Monitor logs**:

```bash
docker-compose logs -f
```

## Configuration

### Required Settings

| Variable | Description                           | Example     |
| -------- | ------------------------------------- | ----------- |
| `UPRN`   | Your Unique Property Reference Number | `123456789` |

### Schedule Settings

| Variable        | Description                         | Default      | Example       |
| --------------- | ----------------------------------- | ------------ | ------------- |
| `CRON_SCHEDULE` | When to run the check (cron format) | `0 18 * * 1` | `0 9 * * 0,3` |

### Discord Notifications

| Variable          | Description                  | Default | Example                                |
| ----------------- | ---------------------------- | ------- | -------------------------------------- |
| `DISCORD_ENABLED` | Enable Discord notifications | `false` | `true`                                 |
| `DISCORD_WEBHOOK` | Discord webhook URL          |         | `https://discord.com/api/webhooks/...` |

### WhatsApp Notifications (CallMeBot)

| Variable           | Description                    | Default | Example        |
| ------------------ | ------------------------------ | ------- | -------------- |
| `WHATSAPP_ENABLED` | Enable WhatsApp notifications  | `false` | `true`         |
| `WHATSAPP_PHONE`   | Phone number with country code |         | `+1234567890`  |
| `WHATSAPP_APIKEY`  | CallMeBot API key              |         | `your-api-key` |

### Email Notifications

| Variable            | Description                        | Default          | Example                 |
| ------------------- | ---------------------------------- | ---------------- | ----------------------- |
| `EMAIL_ENABLED`     | Enable email notifications         | `false`          | `true`                  |
| `EMAIL_SMTP_SERVER` | SMTP server address                | `smtp.gmail.com` | `smtp.outlook.com`      |
| `EMAIL_SMTP_PORT`   | SMTP server port                   | `587`            | `465`                   |
| `EMAIL_SENDER`      | Sender email address               |                  | `sender@example.com`    |
| `EMAIL_PASSWORD`    | Sender email password/app password |                  | `your-app-password`     |
| `EMAIL_RECIPIENT`   | Recipient email address            |                  | `recipient@example.com` |

## How It Works

### Data Retrieval Process

1. **HTTP Request**: Makes authenticated request to Vale of White Horse Council website
2. **HTML Parsing**: Uses BeautifulSoup to extract collection information from specific CSS classes
3. **Data Processing**: Parses collection day, type, and special messages
4. **Error Handling**: Gracefully handles network errors and parsing failures

### Notification Flow

1. **Message Formatting**: Creates appropriate message based on collection data
2. **Multi-Channel Delivery**: Sends to all enabled notification channels
3. **Error Reporting**: Logs success/failure for each notification method

### Container Lifecycle

1. **Startup**: Runs collection check immediately
2. **Cron Setup**: Configures scheduled execution based on `CRON_SCHEDULE`
3. **Continuous Operation**: Runs in background with log monitoring

## Finding Your UPRN

Your UPRN (Unique Property Reference Number) can be found by:

1. **Council Website Method**:

   - Visit [Vale of White Horse Council](https://www.whitehorsedc.gov.uk/)
   - Search for your property in their bin collection service
   - Look for the UPRN in the URL or page source

2. **Alternative Methods**:
   - Check your council tax bill
   - Use online UPRN lookup services
   - Contact the council directly

## Project Structure

```
bin-collection-reminder/
├── 📁 scripts/                 # Main application code
│   ├── bin_collection.py       # Core scraping and orchestration
│   └── notifications.py        # Multi-channel notification services
├── 📁 tests/                   # Test suite
│   ├── __init__.py            # Test package initialization
│   ├── test_beautifulsoup.py  # HTML parsing tests
│   └── CLAUDE.md              # AI assistant guidance
├── 📄 Dockerfile              # Container definition
├── 📄 docker-compose.yml      # Service orchestration
├── 📄 entrypoint.sh           # Container startup script
├── 📄 requirements.txt        # Python dependencies
├── 📄 env.template            # Environment configuration template
├── 📄 .gitignore             # Git ignore patterns
└── 📄 README.md              # This documentation
```

## Development

### Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Run directly
python -m scripts.bin_collection

# Run tests
python -m pytest tests/

# Type checking
mypy scripts/

# Code formatting
black scripts/ tests/
```

### Code Style Guidelines

- **Type Hints**: All functions have complete type annotations
- **Error Handling**: Comprehensive exception handling with timeouts
- **Documentation**: Docstrings with Args/Returns sections
- **Imports**: Organized (standard library → third-party → local)
- **Formatting**: 4-space indentation, 88-character line length

### Testing

```bash
# Run all tests
python -m unittest discover tests/

# Run specific test
python -m unittest tests.test_beautifulsoup

# Run with coverage
python -m coverage run -m unittest discover tests/
python -m coverage report
```

## API Integration Details

### Vale of White Horse Council

- **Endpoint**: `https://eform.southoxon.gov.uk/ebase/BINZONE_DESKTOP.eb`
- **Authentication**: Cookie-based with UPRN
- **Rate Limiting**: Built-in 10-second timeout
- **Response Format**: HTML with specific CSS classes

### CallMeBot WhatsApp API

- **Endpoint**: `https://api.callmebot.com/whatsapp.php`
- **Authentication**: API key required
- **Setup**: [CallMeBot WhatsApp Guide](https://www.callmebot.com/blog/free-api-whatsapp-messages/)

### Discord Webhooks

- **Format**: JSON payload with username customization
- **Rate Limiting**: Respects Discord's webhook limits

## Troubleshooting

### Common Issues

**Container won't start**:

```bash
# Check logs
docker-compose logs bin-collection-reminder

# Verify environment variables
docker-compose config
```

**No notifications received**:

```bash
# Check notification settings
docker exec bin-collection-reminder env | grep -E "(DISCORD|WHATSAPP|EMAIL)"

# Test manually
docker exec bin-collection-reminder python -m scripts.bin_collection
```

**UPRN not working**:

- Verify UPRN is correct (numeric, no spaces)
- Check Vale of White Horse Council website is accessible
- Try running script manually to see error messages

### Debugging

**Enable verbose logging**:

```bash
# Add to docker-compose.yml environment section
- DEBUG=true
```

**Manual execution**:

```bash
# Run script once
docker exec bin-collection-reminder python -m scripts.bin_collection

# Check cron logs
docker exec bin-collection-reminder tail -f /var/log/cron.log
```

## Security Considerations

- **Environment Variables**: Sensitive data stored in `.env` file (not committed)
- **Network Security**: HTTPS requests with proper timeout handling
- **Container Security**: Minimal base image with only required packages
- **Credential Management**: Supports app passwords for email authentication

## Performance

- **Memory Usage**: ~50MB container footprint
- **Network**: Single HTTP request per execution
- **CPU**: Minimal usage (only during scheduled runs)
- **Storage**: Logs rotate automatically

## Contributing

1. **Fork the repository**
2. **Create feature branch**: `git checkout -b feature/amazing-feature`
3. **Follow code style**: Use type hints, docstrings, and error handling
4. **Add tests**: Include unit tests for new functionality
5. **Update documentation**: Keep README and docstrings current
6. **Submit pull request**: Include description of changes

### Development Setup

```bash
# Clone your fork
git clone https://github.com/yourusername/bin-collection-reminder.git

# Install development dependencies
pip install -r requirements.txt
pip install pytest mypy black flake8

# Run quality checks
black scripts/ tests/
flake8 scripts/
mypy scripts/
python -m pytest tests/
```

## License

This project is open source. Please check the repository for license details.

## Acknowledgments

- **Vale of White Horse Council**: For providing accessible bin collection data
- **CallMeBot**: For free WhatsApp API service
- **Discord**: For webhook notification support
- **Python Community**: For excellent libraries (requests, BeautifulSoup, etc.)

## Changelog

### Recent Improvements

- ✅ Added comprehensive type hints
- ✅ Improved error handling with timeouts
- ✅ Enhanced documentation with architecture diagrams
- ✅ Added unit tests for HTML parsing
- ✅ Containerized deployment with Docker
- ✅ Multi-channel notification support
- ✅ Configurable scheduling via environment variables

### Roadmap

- 🔄 Add more comprehensive test coverage
- 🔄 Implement retry logic for failed notifications
- 🔄 Add support for multiple UPRNs
- 🔄 Create web dashboard for configuration
- 🔄 Add Prometheus metrics for monitoring
