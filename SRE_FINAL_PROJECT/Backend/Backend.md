Got it! Here's your **Backend README** with all `**bold formatting**` removed for a cleaner look, while still keeping the structure, emojis, and code blocks:

---

```markdown
# 🌟 Backend README – IPC Nexus

## 🚀 Project Overview

The backend of the ipc_nexus project powers core functionality, handling API requests and database interactions.  
Built with Flask (Python) and Gunicorn, it uses a SQLite database (`law_enforcement.db`) and exposes metrics for Prometheus monitoring.

---

## ✅ Prerequisites

Make sure you have:

- Python (v3.8 or later)
- pip (for package management)
- SQLite (for database operations)
- Docker and Minikube (for containerized deployment)
- kubectl (for Kubernetes management)
- Git (for version control)
- An API testing tool (e.g., Postman or `curl`)

---

## 🛠️ Installation

### 🔹 Clone the repository:

```bash
git clone git clone https://github.com/HafsaZareen/MTHREE-TRAINING-NOTES.git
cd SRE_FINAL_PROJECT/Backend
```

### 🔹 Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate         # On Windows: venv\Scripts\activate
```

### 🔹 Install dependencies:

```bash
pip install -r requirements.txt
```

### 🔹 Set up environment variables:

- Create a `.env` file in the `Backend` directory.
- Add the following:

```env
FLASK_APP=Flask_backend/app.py
FLASK_ENV=development
DATABASE_URL=sqlite:///law_enforcement.db
```

---

## 🎮 Usage

### 🧪 Local Development

Start the Flask server:

```bash
flask run
```

- Access the API at: http://localhost:5000
- Test metrics endpoint:

```bash
curl http://localhost:5000/metrics
```

---

### ☸️ Kubernetes Deployment

Start Minikube:

```bash
minikube start
```

Apply the backend deployment:

```bash
kubectl apply -f ~/ipc_nexus/k8s/backend.yaml
```

Forward the backend service port:

```bash
kubectl port-forward service/backend-service 5000:5000
```

Access the API at: http://localhost:5000

---

### 🗃️ Database Management

Copy the SQLite database from the backend pod (replace `<pod-name>` with the actual pod name):

```bash
kubectl cp <pod-name>:/app/Database/law_enforcement.db ./law_enforcement.db
```

To remove and refresh the local database:

```bash
rm law_enforcement.db
kubectl cp <pod-name>:/app/Database/law_enforcement.db ./law_enforcement.db
```

---

### 🧯 Troubleshooting

Check backend pod status:

```bash
kubectl get pods
```

View logs:

```bash
kubectl logs -l app=backend
```

Describe a specific pod:

```bash
kubectl describe pod <pod-name>
```

---

## 📂 Folder Structure

```
Backend/
├── Database/                   # Database scripts/migrations
├── Dataset/                    # Datasets for processing/ML
├── Flask_backend/              # Flask app code
├── prometheus-deployment.yaml  # Prometheus config 🌡️
├── Dockerfile                  # Docker config
├── requirements.txt            # Python dependencies
├── to/                         # Misc/temp files
├── venv/                       # Virtual env
```

---

## 🤝 Contributing

1. Fork the repository.
2. Create a new branch:

   ```bash
   git checkout -b feature/your-feature
   ```

3. Commit your changes:

   ```bash
   git commit -m "Add your feature"
   ```

4. Push to the branch:

   ```bash
   git push origin feature/your-feature
   ```

5. Open a Pull Request.

---

## 📧 Contact

Reach out at: <hafsazareen064@gmail.com>
```
