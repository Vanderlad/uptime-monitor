# Website Uptime Monitor (Python)

A lightweight Python-based uptime monitoring tool that periodically checks one or more websites, logs their status, and sends real-time alerts to Discord when downtime or errors are detected.

Designed as a simple, configurable automation tool that runs unattended on a Linux server using cron.

---

## Features

- Monitor multiple websites or endpoints
- Configurable timeout, retries, and valid HTTP status ranges
- Logs uptime checks with timestamps and response times
- Sends Discord webhook alerts on failures
- Graceful error handling (network errors, timeouts, invalid responses)
- Exit codes suitable for cron and automation workflows
