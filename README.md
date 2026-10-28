# Zero Trust Access Anomaly Detector

NGINX acts as an L7 proxy in front of FastAPI services. It validates JWTs at the edge,
rejects bad tokens, and logs every rejection for audit. A Python detector tails a live
Prometheus stream and flags request spikes, logins from unusual locations, and token reuse.
Grafana shows Zero Trust policy activity in real time. Everything runs from one Docker Compose file.

**Stack:** Python, FastAPI, NGINX, JWT/OAuth2, Prometheus, Grafana, Docker

## Build progress
- [x] Step 1: FastAPI backend + demo token issuer
- [ ] Step 2: NGINX JWT edge proxy
- [ ] Step 3: Prometheus metrics + scrape config
- [ ] Step 4: Anomaly detector
- [ ] Step 5: Grafana dashboard + Docker Compose
