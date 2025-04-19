
```markdown
# SRE README 🛡️

## Project Overview 🚀  
The **Site Reliability Engineering (SRE)** component of `ipc_nexus` ensures the system’s reliability, scalability, and performance. It uses **Prometheus** for monitoring and **Grafana** for visualization, focusing on maintaining service availability and responding to incidents.

---

## Role in ipc_nexus 🌟  

SRE handles:

- Monitoring backend and frontend health with Prometheus (`prometheus-deployment.yaml`)
- Visualizing metrics in Grafana (namespace `ipcmonitoring`)
- Setting up alerts and incident response processes
- Ensuring service-level objectives (SLOs) for uptime and performance

> Note: Unlike DevOps, which focuses on deployment automation, SRE prioritizes system reliability and observability post-deployment.

---

## Prerequisites ✅  

Make sure the following are installed:

- Prometheus for monitoring  
- Grafana for visualization  
- Docker and Minikube for local infrastructure  
- kubectl for managing Kubernetes clusters  
- Git for version control

---

## Installation 🛠️  

### Clone the repository:
```bash
git clone https://github.com/HafsaZareen/MTHREE-TRAINING-NOTES.git
cd MTHREE-TRAINING-NOTES/SRE_FINAL_PROJECT
```

### Deploy Prometheus:
```bash
kubectl apply -f Backend/prometheus-deployment.yaml
```

### Deploy Grafana:
Make sure Grafana is deployed in the `ipcmonitoring` namespace.

### Forward Grafana service:
```bash
kubectl port-forward -n ipcmonitoring service/grafana 3000:80
```

---

## Usage 🎮  

### Access Prometheus:

#### Forward Prometheus service:
```bash
kubectl port-forward svc/prometheus-service 9090:9090
```

#### Visit:
- [http://localhost:9090/targets](http://localhost:9090/targets) — View all scrape targets  
- [http://localhost:9090/targets?search=](http://localhost:9090/targets?search=) — Filter specific targets  
- [http://localhost:5000/metrics](http://localhost:5000/metrics) — Backend metrics

---

### Access Grafana:

- Visit: [http://localhost:3000](http://localhost:3000)
- Add Prometheus as a data source: `http://prometheus-service:9090`

---

## Configure Alerts 🔔  

- Edit alerting rules inside `prometheus-deployment.yaml`
- (Optional) Set up Alertmanager for notifications via Slack, email, etc.

---

## Monitoring Details 🌡️  

- **Backend**:
  - Scrapes metrics from `/metrics` on port `5000`
  - Includes liveness/readiness probes at `/nlp/test`

- **Frontend**:
  - Exposes Nginx metrics on port `9113` via a Prometheus exporter

---

## Folder Structure 📂  

```
ipc_nexus/
├── Backend/prometheus-deployment.yaml  # Prometheus configuration
├── k8s/                                # Kubernetes manifests (SRE-related)
```

---

## Contributing 🤝  

1. Fork the repository  
2. Create a new branch:  
   ```bash
   git checkout -b feature/your-feature
   ```
3. Commit your changes:  
   ```bash
   git commit -m "Add your feature"
   ```
4. Push the branch:  
   ```bash
   git push origin feature/your-feature
   ```
5. Open a Pull Request 🚀

---

## Contact 📧  
Reach out at: hafsazareen064@gmail.com


```

