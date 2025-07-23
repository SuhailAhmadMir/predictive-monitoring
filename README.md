# 🔧 Automated Monitoring & Ticketing Integration

This project demonstrates how to automate alert-based ticketing using **Prometheus**, **Alertmanager**, and **Zammad**, orchestrated via **Docker Compose**. The system monitors application health and dynamically generates support tickets when thresholds are breached — enabling fast response through an integrated observability and incident management pipeline.

---

## 📌 Key Components

| Tool            | Role                                                                 |
|-----------------|----------------------------------------------------------------------|
| **Prometheus**  | Scrapes metrics from services and triggers alerts                    |
| **Alertmanager**| Manages alert routing and grouping                                   |
| **Zammad**      | Open-source ticketing system where alerts are logged as tickets      |
| **Flask Webhook** | Listens to Alertmanager alerts and forwards them to Zammad API     |
| **Grafana**     | Visualizes metrics and alerts using rich dashboards                  |
| **Docker Compose** | Manages and runs all services as containers                        |

---

## 📁 Directory Structure

```bash
predictive-monitoring-poc/
├── alertmanager/
│   └── config.yml
├── app/
│   └── your-app (sample app emitting metrics)
├── docker/
│   └── Dockerfiles / scripts
├── docker-compose.yml
├── grafana/
│   └── dashboards, provisioning, etc.
├── prometheus/
│   └── prometheus.yml
└── zammad-hook/
    ├── alertmanager-zammad-hook.py
    ├── requirements.txt
    └── Dockerfile
