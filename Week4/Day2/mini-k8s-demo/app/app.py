# Simple Flask application for Kubernetes demonstration
from flask import Flask, jsonify
import os
import socket
import datetime

# Initialize Flask application
app = Flask(__name__)

# Read configuration from environment variables (will be set via Kubernetes ConfigMap)
APP_NAME = os.environ.get('APP_NAME', 'mini-k8s-demo')
APP_VERSION = os.environ.get('APP_VERSION', '1.0.0')

# Track request count to demonstrate statelessness in Kubernetes
request_count = 0

@app.route('/')
def index():
    """Main page showing container/pod information"""
    global request_count
    request_count += 1
    
    # Return HTML with pod information - demonstrates how each pod is a separate instance
    return f"""
    <h1>Kubernetes Mini Demo</h1>
    <p>App: {APP_NAME} v{APP_VERSION}</p>
    <p>Hostname (Pod name): {socket.gethostname()}</p>
    <p>Pod IP: {socket.gethostbyname(socket.gethostname())}</p>
    <p>Request count: {request_count}</p>
    <p>Time: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
    
    <p><a href="/api/info">View API Info</a></p>
    <p><a href="/api/health">Health Check</a></p>
    """

@app.route('/api/info')
def api_info():
    """API endpoint returning application information"""
    return jsonify({
        'name': APP_NAME,
        'version': APP_VERSION,
        'hostname': socket.gethostname(),
        'request_count': request_count
    })

@app.route('/api/health')
def health_check():
    """Health check endpoint for Kubernetes liveness and readiness probes"""
    return jsonify({
        'status': 'healthy',
        'time': datetime.datetime.now().isoformat(),
        'hostname': socket.gethostname()
    })

if __name__ == '__main__':
    # Start the Flask application
    port = int(os.environ.get('PORT', 5000))
    print(f"Starting {APP_NAME} v{APP_VERSION} on port {port}")
    app.run(host='0.0.0.0', port=port)
