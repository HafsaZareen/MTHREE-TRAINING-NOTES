
```markdown
# DevOps README ⚙️

## Project Overview 🚀  
The DevOps component of `ipc_nexus` focuses on automating the build, test, and deployment pipeline to deliver the backend and frontend efficiently. It uses **Docker** for containerization, **Kubernetes** for orchestration, and **Minikube** for local testing, ensuring rapid and consistent deployments.

---

## Role in ipc_nexus 🌟  
DevOps handles:

- Building and deploying containerized applications (Dockerfile for backend/frontend)
- Managing Kubernetes deployments (`backend.yaml`, `frontend.yaml`) and services (`frontend-service.yaml`)
- Setting up CI/CD pipelines and local development with Docker Compose
- Exposing services for development and testing (e.g., port-forwarding)

> Note: Unlike SRE, which focuses on system reliability and monitoring, DevOps prioritizes streamlined delivery from code to production.

---

## Prerequisites ✅  

Ensure you have:

- Docker (v20.x or later)  
- Minikube for local Kubernetes  
- kubectl for cluster management  
- Git for version control  
- CI/CD tool (e.g., GitHub Actions, Jenkins)

---

## Installation 🛠️  

### Clone the repository:
```bash
git clone https://github.com/HafsaZareen/MTHREE-TRAINING-NOTES.git
cd MTHREE-TRAINING-NOTES/SRE_FINAL_PROJECT
```

### Start Minikube:
```bash
minikube start
```

### Set up Docker Compose (local multi-container):
```bash
docker-compose build
docker-compose up
```

### Deploy Kubernetes manifests:
```bash
kubectl apply -f k8s/backend.yaml
kubectl apply -f k8s/frontend.yaml
kubectl apply -f k8s/frontend-service.yaml
kubectl apply -f Backend/prometheus-deployment.yaml
```

---

## Usage 🎮  

### Local Docker Compose:
```bash
docker-compose up
```

### Kubernetes with Minikube:

#### Forward service ports:
```bash
kubectl port-forward service/backend-service 5000:5000
kubectl port-forward service/frontend-service 3001:80
kubectl port-forward -n ipcmonitoring service/grafana 3000:80
kubectl port-forward svc/prometheus-service 9090:9090
```

#### Access services:
- Backend: [http://localhost:5000](http://localhost:5000)  
- Frontend: [http://localhost:3001](http://localhost:3001)  
  - Example: [http://localhost:3001/policeinfo](http://localhost:3001/policeinfo)  
- Grafana: [http://localhost:3000](http://localhost:3000)  
- Prometheus: [http://localhost:9090](http://localhost:9090)

---

## Troubleshooting 🔧  

### Check pod status:
```bash
kubectl get pods
```

### Describe a pod (replace `<pod-name>`):
```bash
kubectl describe pod <pod-name>
```

---

## Kubernetes Manifests 📜  

- **Backend Deployment**:  
  Runs Flask with Gunicorn, mounts `db-pvc` and `uploads-pvc`, exposes port 5000 with `/nlp/test` probes.

- **Frontend Deployment**:  
  Runs Nginx with a Prometheus exporter on port 9113.

- **Frontend Service**:  
  Exposes port 80 (HTTP) and 9113 (metrics) via NodePort.

---

## Folder Structure 📂  

```
ipc_nexus/
├── Backend/Dockerfile      # Backend Docker config
├── Frontend/Dockerfile     # Frontend Docker config
├── k8s/                    # Kubernetes manifests
├── docker-compose.yml      # Local multi-container setup
```

---

## Contributing 🤝  

- Fork the repository  
- Create a new branch:  
  ```bash
  git checkout -b feature/your-feature
  ```
- Commit your changes:  
  ```bash
  git commit -m "Add your feature"
  ```
- Push your branch:  
  ```bash
  git push origin feature/your-feature
  ```
- Open a Pull Request

---

## Contact 📧  
Reach out at: `hafsazareen064@gmail.com`
```

---

