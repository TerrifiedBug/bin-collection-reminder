FROM python:3.9-slim
WORKDIR /app

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    cron \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* \
    && rm -rf /tmp/* /var/tmp/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt && \
    rm -rf /root/.cache/pip/*

COPY scripts/ /app/scripts/
COPY entrypoint.sh /usr/local/bin/entrypoint.sh
RUN chmod +x /usr/local/bin/entrypoint.sh

# Default environment variables
ENV UPRN=""
ENV CRON_SCHEDULE="0 18 * * 1"
ENV DISCORD_ENABLED=false
ENV DISCORD_WEBHOOK=""
ENV WHATSAPP_ENABLED=false
ENV WHATSAPP_PHONE=""
ENV WHATSAPP_APIKEY=""
ENV EMAIL_ENABLED=false
ENV EMAIL_SMTP_SERVER="smtp.gmail.com"
ENV EMAIL_SMTP_PORT=587
ENV EMAIL_SENDER=""
ENV EMAIL_PASSWORD=""
ENV EMAIL_RECIPIENT=""

ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]
