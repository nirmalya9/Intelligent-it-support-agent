# Internal application incident troubleshooting

Symptoms: application unavailable, HTTP 5xx errors, slow response, or timeouts.

1. Record the application name, URL, timestamp, error text, and whether other users are affected.
2. Check the published service status page if available.
3. Retry once after confirming the issue is not transient. Avoid repeated retries that could worsen an incident.
4. For HTTP 500 or 503 errors, capture a request ID if shown and route the issue to application support.
5. Do not paste credentials, tokens, or personal data into tickets.
6. If multiple users or a business-critical service are affected, escalate using the incident process.
