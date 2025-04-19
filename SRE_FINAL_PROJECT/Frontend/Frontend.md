

```markdown
# 🌈 Frontend README – IPC Nexus

## 🚀 Project Overview

The frontend of the **IPC Nexus** project delivers a user-friendly interface to interact with backend APIs.  
Built with **Vite** for fast development, it uses **Nginx** for production serving and is linted with **ESLint** for code quality.

---

## ✅ Prerequisites

Make sure you have the following installed:

- **Node.js** (v16.x or later)
- **npm** (v8.x or later)
- **Docker** (optional, for containerized deployment)
- **Git** (for version control)
- A modern web browser (e.g., **Chrome**, **Firefox**)

---

## 🛠️ Installation

1. **Clone the repository:**

   ```bash
   git clone <repository-url>
   cd ipc_nexus/Frontend
   ```

2. **Install dependencies:**

   ```bash
   npm install
   ```

3. **Set up environment variables:**

   - Create a `.env` file in the `Frontend` directory.
   - Add the following:

     ```env
     VITE_API_URL=http://localhost:5000/api
     ```

---

## 🎮 Usage

### 🧪 Start the development server:

```bash
npm run dev
```

- Open [http://localhost:5173](http://localhost:5173) in your browser.

---

### 🚀 For production:

```bash
npm run build
docker build -t ipc_nexus_frontend .
docker run -p 80:80 ipc_nexus_frontend
```

- Access the production build at [http://localhost](http://localhost)

---

## 📂 Folder Structure

```
Frontend/
├── public/             # Static assets (favicon, images)
├── src/                # Source code (components, pages)
├── node_modules/       # Node.js dependencies
├── Dockerfile          # Docker config
├── eslint.config.js    # ESLint config 🧹
├── index.html          # Main HTML entry
├── nginx.conf          # Nginx config
├── package.json        # Dependencies/scripts
├── package-lock.json   # Locked dependency versions
├── vite.config.js      # Vite config
```

---



