#!/usr/bin/env python3
"""
Kubernetes Master Application
=============================

This Flask application demonstrates:
1. Reading from and writing to mounted volumes
2. Working with environment variables (from ConfigMaps and Secrets)
3. Health checking
4. Resource usage reporting
5. Metrics collection

This showcases how a containerized application interacts with Kubernetes features.
"""
# Flask: The core class to create a Flask web application.
# jsonify: Used to convert Python objects (like dictionaries) into JSON responses.
# render_template_string: Allows rendering HTML templates from string inputs.
# request: Handles incoming HTTP requests (e.g., form data, query parameters).
# redirect, url_for: Helps redirect users to different routes within the application.
from flask import Flask, jsonify, render_template_string, request, redirect, url_for
import os #Interact with the operating system (e.g., environment variables, file handling).
import socket # Handles network-related tasks (e.g., getting hostnames, IP addresses).
import datetime #Works with date and time (e.g., logging timestamps, calculating uptime).
import json #Enables JSON encoding and decoding.
import logging  #Manages logging messages (e.g., debugging, error tracking).
import uuid #Generates unique identifiers (e.g., session IDs, transaction IDs).
import platform # Retrieves system information (OS, architecture, etc.).
import psutil  # For resource usage statistics , Monitors system resources like CPU, memory, disk usage, etc.
import time # Provides time-related functions (e.g., sleep, timestamps).
import threading # Allows running background tasks asynchronously.
import sys #Provides system-specific functions (e.g., exiting the program, checking Python version).

# Initialize Flask application
app = Flask(__name__)

log_file = os.path.join(os.environ.get('LOG_PATH', '/logs'), 'app.log')
logging.basicConfig(
    
    level=logging.INFO,#logging.INFO stores logs of levels INFO, WARNING, ERROR, and CRITICAL will be recorded, but DEBUG messages will be ignored.
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),#outputs logs to the console.
        logging.FileHandler(log_file)#Saves logs to the specified file (app.log).

    ]
)

logger = logging.getLogger('k8s-master-app')#Creates a named logger called "k8s-master-app"

# Read configuration from environment variables (from ConfigMaps)
APP_NAME = os.environ.get('APP_NAME', 'k8s-master-app')
APP_VERSION = os.environ.get('APP_VERSION', '1.0.0')
ENVIRONMENT = os.environ.get('ENVIRONMENT', 'development')
DATA_PATH = os.environ.get('DATA_PATH', '/data')
CONFIG_PATH = os.environ.get('CONFIG_PATH', '/config')
LOG_PATH = os.environ.get('LOG_PATH', '/logs')

# Read secrets from environment variables (from Secrets)
# In a real app, these would be more sensitive values like API keys
SECRET_KEY = os.environ.get('SECRET_KEY', 'default-dev-key')
DB_PASSWORD = os.environ.get('DB_PASSWORD', 'default-password')

# Generate a (uui-Universally Unique Identifier)unique instance ID to demonstrate statelessness ,each pod gets a unique INSTANCE_ID for logging/debugging.
INSTANCE_ID = str(uuid.uuid4())[:8]

# Track request count and application metrics
# Performance Monitoring: Helps measure how many requests/errors occur.
# Can be exported to Prometheus or other monitoring tool
request_count = 0
start_time = time.time()
metrics = {
    'requests': 0,
    'errors': 0,
    'data_reads': 0,
    'data_writes': 0
}

# Simulate application load for resource usage demonstration,Runs a background task that continuously performs some CPU work.
#Logs debug messages every 1000 iterations.(Useful for Kubernetes auto-scaling )
def background_worker():
    """
    Simulate background work to demonstrate resource usage.
    In a real app, this might be processing tasks, etc.
    """
    logger.info("Background worker started")
    counter = 0
    while True:
        # Simple CPU work - calculate prime numbers
        counter += 1
        if counter % 1000 == 0:
            # Log occasionally to show activity
            logger.debug(f"Background worker tick: {counter}")
        time.sleep(0.1)  # Don't use too much CPU

# Start the background worker
worker_thread = threading.Thread(target=background_worker, daemon=True)
worker_thread.start()

@app.route('/')
def index():
    """Main page showing application status and mounted volume information"""
    global request_count, metrics
    request_count += 1
    metrics['requests'] += 1
    
    # Log the request
    logger.info(f"Request to index page from {request.remote_addr}")
    
    # Get system information
    system_info = {
        'hostname': socket.gethostname(),#Unique name of the instance.
        'platform': platform.platform(),# OS information.
        'python_version': platform.python_version(),
        'cpu_count': psutil.cpu_count(),#Number of CPU cores.
        'memory': f"{psutil.virtual_memory().total / (1024 * 1024):.1f} MB",#Total RAM available.
        'uptime': f"{time.time() - start_time:.1f} seconds"# How long the container has been running.

    }
    
    # Get resource usage Helps in troubleshooting high resource usage.
    resource_usage = {
        'cpu_percent': psutil.cpu_percent(),
        'memory_percent': psutil.virtual_memory().percent,
        'disk_usage': f"{psutil.disk_usage('/').percent}%"
    }
    
    # Get information about mounted volumes
    volumes = {}
    #   volumes allow data to persist across restarts  

    # Check data volume
    try:
        data_files = os.listdir(DATA_PATH)
        volumes['data'] = {
            'path': DATA_PATH,#Tries to list files in the DATA_PATH volume.
            'files': data_files,#If successful, it stores the list of files.
            'status': 'mounted' if data_files else 'empty'#If an error occurs, it logs the error and increments metrics['errors'].
        }
        metrics['data_reads'] += 1

    except Exception as e:
        volumes['data'] = {
            'path': DATA_PATH,
            'error': str(e),
            'status': 'error'
        }
        metrics['errors'] += 1
    
    # Check config volume
    try:
        config_files = os.listdir(CONFIG_PATH)
        volumes['config'] = {
            'path': CONFIG_PATH,
            'files': config_files,
            'status': 'mounted' if config_files else 'empty'
        }
    except Exception as e:
        volumes['config'] = {
            'path': CONFIG_PATH,
            'error': str(e),
            'status': 'error'
        }
        metrics['errors'] += 1
    
    # Check logs volume
    try:
        logs_files = os.listdir(LOG_PATH)
        volumes['logs'] = {
            'path': LOG_PATH,
            'files': logs_files,
            'status': 'mounted' if logs_files else 'empty'
        }
    except Exception as e:
        volumes['logs'] = {
            'path': LOG_PATH,
            'error': str(e),
            'status': 'error'
        }
        metrics['errors'] += 1

    # Build HTML content using a template
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>{{ app_name }} - Kubernetes Master App</title>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            body { 
                font-family: Arial, sans-serif; 
                line-height: 1.6; 
                margin: 0; 
                padding: 20px; 
                background-color: #f5f5f5;
                color: #333;
            }
            h1, h2, h3 { color: #2c3e50; }
            .container { 
                max-width: 1000px; 
                margin: 0 auto; 
                background-color: white;
                padding: 20px;
                border-radius: 8px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }
            .info-box { 
                background-color: #f8f9fa; 
                border-radius: 5px; 
                padding: 15px; 
                margin-bottom: 20px; 
                border-left: 4px solid #3498db;
            }
            .success { color: #27ae60; }
            .error { color: #e74c3c; }
            .warning { color: #f39c12; }
            .info { color: #3498db; }
            .file-list { 
                background-color: #f9f9f9; 
                border-radius: 5px; 
                padding: 10px; 
                border: 1px solid #ddd;
            }
            .file-item {
                display: flex;
                justify-content: space-between;
                padding: 5px 10px;
                border-bottom: 1px solid #eee;
            }
            .file-item:last-child {
                border-bottom: none;
            }
            .nav-links {
                display: flex;
                gap: 10px;
                margin-top: 20px;
            }
            .nav-link {
                display: inline-block;
                padding: 8px 16px;
                background-color: #3498db;
                color: white;
                text-decoration: none;
                border-radius: 4px;
                font-weight: bold;
                transition: background-color 0.3s;
            }
            .nav-link:hover {
                background-color: #2980b9;
            }
            .metrics {
                display: flex;
                gap: 10px;
                flex-wrap: wrap;
            }
            .metric-card {
                flex: 1;
                min-width: 120px;
                background-color: #fff;
                padding: 15px;
                border-radius: 8px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                text-align: center;
            }
            .metric-value {
                font-size: 24px;
                font-weight: bold;
                margin: 10px 0;
                color: #3498db;
            }
            .metric-label {
                font-size: 14px;
                color: #7f8c8d;
            }
            .badge {
                display: inline-block;
                padding: 3px 8px;
                border-radius: 12px;
                font-size: 12px;
                font-weight: bold;
                color: white;
                background-color: #95a5a6;
            }
            .badge-primary { background-color: #3498db; }
            .badge-success { background-color: #27ae60; }
            .badge-warning { background-color: #f39c12; }
            .badge-danger { background-color: #e74c3c; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>{{ app_name }} <span class="badge badge-primary">v{{ app_version }}</span></h1>
            <p>A comprehensive Kubernetes demonstration application</p>
            
            <div class="info-box">
                <h2>Pod Information</h2>
                <p><strong>Instance ID:</strong> {{ instance_id }}</p>
                <p><strong>Hostname:</strong> {{ system_info.hostname }}</p>
                <p><strong>Environment:</strong> <span class="badge badge-success">{{ environment }}</span></p>
                <p><strong>Request count:</strong> {{ request_count }}</p>
                <p><strong>Platform:</strong> {{ system_info.platform }}</p>
                <p><strong>Uptime:</strong> {{ system_info.uptime }}</p>
            </div>
            
            <div class="info-box">
                <h2>Resource Usage</h2>
                <div class="metrics">
                    <div class="metric-card">
                        <div class="metric-label">CPU Usage</div>
                        <div class="metric-value">{{ resource_usage.cpu_percent }}%</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-label">Memory</div>
                        <div class="metric-value">{{ resource_usage.memory_percent }}%</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-label">Disk</div>
                        <div class="metric-value">{{ resource_usage.disk_usage }}</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-label">Requests</div>
                        <div class="metric-value">{{ metrics.requests }}</div>
                    </div>
                </div>
            </div>
            
            <div class="info-box">
                <h2>Mounted Volumes</h2>
                
                <h3>Data Volume</h3>
                <p><strong>Path:</strong> {{ volumes.data.path }}</p>
                <p><strong>Status:</strong> 
                    {% if volumes.data.status == 'mounted' %}
                        <span class="success">Successfully mounted</span>
                    {% elif volumes.data.status == 'empty' %}
                        <span class="warning">Mounted but empty</span>
                    {% else %}
                        <span class="error">Error: {{ volumes.data.error }}</span>
                    {% endif %}
                </p>
                
                {% if volumes.data.files %}
                <div class="file-list">
                    <h4>Files:</h4>
                    {% for file in volumes.data.files %}
                    <div class="file-item">
                        <span>{{ file }}</span>
                        <a href="/view-file?path={{ volumes.data.path }}/{{ file }}" class="nav-link">View</a>
                    </div>
                    {% endfor %}
                </div>
                {% endif %}
                
                <h3>Config Volume</h3>
                <p><strong>Path:</strong> {{ volumes.config.path }}</p>
                <p><strong>Status:</strong> 
                    {% if volumes.config.status == 'mounted' %}
                        <span class="success">Successfully mounted</span>
                    {% elif volumes.config.status == 'empty' %}
                        <span class="warning">Mounted but empty</span>
                    {% else %}
                        <span class="error">Error: {{ volumes.config.error }}</span>
                    {% endif %}
                </p>
                
                {% if volumes.config.files %}
                <div class="file-list">
                    <h4>Files:</h4>
                    {% for file in volumes.config.files %}
                    <div class="file-item">
                        <span>{{ file }}</span>
                        <a href="/view-file?path={{ volumes.config.path }}/{{ file }}" class="nav-link">View</a>
                    </div>
                    {% endfor %}
                </div>
                {% endif %}
                
                <h3>Logs Volume</h3>
                <p><strong>Path:</strong> {{ volumes.logs.path }}</p>
                <p><strong>Status:</strong> 
                    {% if volumes.logs.status == 'mounted' %}
                        <span class="success">Successfully mounted</span>
                    {% elif volumes.logs.status == 'empty' %}
                        <span class="warning">Mounted but empty</span>
                    {% else %}
                        <span class="error">Error: {{ volumes.logs.error }}</span>
                    {% endif %}
                </p>
                
                {% if volumes.logs.files %}
                <div class="file-list">
                    <h4>Files:</h4>
                    {% for file in volumes.logs.files %}
                    <div class="file-item">
                        <span>{{ file }}</span>
                        <a href="/view-file?path={{ volumes.logs.path }}/{{ file }}" class="nav-link">View</a>
                    </div>
                    {% endfor %}
                </div>
                {% endif %}
            </div>
            
            <div class="info-box">
                <h2>Actions</h2>
                <div class="nav-links">
                    <a href="/create-file" class="nav-link">Create a File</a>
                    <a href="/api/info" class="nav-link">API Info</a>
                    <a href="/api/health" class="nav-link">Health Check</a>
                    <a href="/api/metrics" class="nav-link">Metrics</a>
                </div>
            </div>
            
            <div class="info-box">
                <h2>Environment Variables</h2>
                <p><strong>APP_NAME:</strong> {{ app_name }}</p>
                <p><strong>APP_VERSION:</strong> {{ app_version }}</p>
                <p><strong>ENVIRONMENT:</strong> {{ environment }}</p>
                <p><strong>DATA_PATH:</strong> {{ data_path }}</p>
                <p><strong>CONFIG_PATH:</strong> {{ config_path }}</p>
                <p><strong>LOG_PATH:</strong> {{ log_path }}</p>
                <p><strong>SECRET_KEY:</strong> {{ secret_key|truncate(10, True, '...') }}</p>
            </div>
        </div>
    </body>
    </html>
    """
    
    # Render the template with our data (render_template_string library helps rendering HTML templates from string inputs)
    return render_template_string(
        html_content,
        app_name=APP_NAME,
        app_version=APP_VERSION,
        environment=ENVIRONMENT,
        instance_id=INSTANCE_ID,
        system_info=system_info,
        resource_usage=resource_usage,
        volumes=volumes,
        request_count=request_count,
        metrics=metrics,
        data_path=DATA_PATH,
        config_path=CONFIG_PATH,
        log_path=LOG_PATH,
        secret_key=SECRET_KEY
    )

@app.route('/view-file')
def view_file():
    """View the contents of a file from a mounted volume"""
    global metrics
    
    # Get the file path from the query parameters
    file_path = request.args.get('path', '')
    
    # Security check to prevent directory traversal attacks
    # Only allow access to our mounted volumes
    allowed_paths = [DATA_PATH, CONFIG_PATH, LOG_PATH]
    valid_path = False
    
    for path in allowed_paths:
        if file_path.startswith(path):
            valid_path = True
            break
    
    if not valid_path:
        metrics['errors'] += 1
        return "Access denied: Invalid path", 403
    
    # Try to read the file
    try:
        with open(file_path, 'r') as f:
            content = f.read()
        
        # Record the successful read
        metrics['data_reads'] += 1
        logger.info(f"File viewed: {file_path}")
        
        # Simple HTML to display the file content
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>File: {os.path.basename(file_path)}</title>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; padding: 20px; }}
                pre {{ background-color: #f8f9fa; padding: 15px; border-radius: 5px; overflow-x: auto; }}
                .nav-link {{
                    display: inline-block;
                    padding: 8px 16px;
                    background-color: #3498db;
                    color: white;
                    text-decoration: none;
                    border-radius: 4px;
                    font-weight: bold;
                }}
            </style>
        </head>
        <body>
            <h1>File: {os.path.basename(file_path)}</h1>
            <p>Path: {file_path}</p>
            <pre>{content}</pre>
            <a href="/" class="nav-link">Back to Home</a>
        </body>
        </html>
        """
        return html
    except Exception as e:
        metrics['errors'] += 1
        logger.error(f"Error viewing file {file_path}: {str(e)}")
        return f"Error reading file: {str(e)}", 500

@app.route('/create-file', methods=['GET', 'POST'])
def create_file():
    """Create a new file in the mounted data volume"""
    global metrics
    
    if request.method == 'POST':
        filename = request.form.get('filename', '')
        content = request.form.get('content', '')
        
        # Only allow creating files in the data directory
        file_path = os.path.join(DATA_PATH, filename)
        
        # For security, don't allow directory traversal
        #This security check prevents directory traversal attacks by ensuring the file is created only inside the allowed DATA_PATH directory.
        if '..' in filename or '/' in filename:
            metrics['errors'] += 1
            return "Invalid filename. Directory traversal not allowed.", 400
        
        try:
            with open(file_path, 'w') as f:
                f.write(content)
            
            # Record the successful write
            metrics['data_writes'] += 1
            logger.info(f"File created: {file_path}")
            
            # Also write to the log volume to demonstrate multiple volume mounting
            log_message = f"File created: {filename} at {datetime.datetime.now().isoformat()}\n"
            with open(os.path.join(LOG_PATH, 'file_operations.log'), 'a') as log:
                log.write(log_message)
            
            return redirect('/')

        except Exception as e:
            metrics['errors'] += 1
            logger.error(f"Error creating file {file_path}: {str(e)}")
            return f"Error creating file: {str(e)}", 500
    else:
        # Show form for creating a file
        html = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Create File</title>
            <style>
                body { font-family: Arial, sans-serif; line-height: 1.6; padding: 20px; }
                .form-group { margin-bottom: 15px; }
                label { display: block; margin-bottom: 5px; }
                input[type="text"], textarea {
                    width: 100%;
                    padding: 8px;
                    border: 1px solid #ddd;
                    border-radius: 4px;
                }
                textarea { height: 200px; }
                button {
                    padding: 8px 16px;
                    background-color: #3498db;
                    color: white;
                    border: none;
                    border-radius: 4px;
                    cursor: pointer;
                    font-weight: bold;
                }
                .nav-link {
                    display: inline-block;
                    padding: 8px 16px;
                    background-color: #95a5a6;
                    color: white;
                    text-decoration: none;
                    border-radius: 4px;
                    font-weight: bold;
                }
            </style>
        </head>
        <body>
            <h1>Create a New File</h1>
            <p>This file will be saved to the mounted data volume.</p>
            
            <form method="post">
                <div class="form-group">
                    <label for="filename">Filename:</label>
                    <input type="text" id="filename" name="filename" required placeholder="example.txt">
                </div>
                
                <div class="form-group">
                    <label for="content">Content:</label>
                    <textarea id="content" name="content" required placeholder="Enter file content here..."></textarea>
                </div>
                
                <div class="form-group">
                    <button type="submit">Create File</button>
                    <a href="/" class="nav-link">Cancel</a>
                </div>
            </form>
        </body>
        </html>
        """
        return html

@app.route('/api/info')
def api_info():
    """API endpoint returning application information"""
    return jsonify({
        'app_name': APP_NAME,
        'version': APP_VERSION,
        'environment': ENVIRONMENT,
        'instance_id': INSTANCE_ID,
        'hostname': socket.gethostname(),
        'request_count': request_count,
        'uptime_seconds': time.time() - start_time,
# Kubernetes volumes allow persistent storage across container restarts.
# Volumes are mounted inside a container as directories.
# This lets the application store logs, config files, and data that persist beyond container restarts.

#Volumes are defined in your Kubernetes YAML files (deployment.yaml or volumes.yaml):
        'volumes': {
            'data': {
                'path': DATA_PATH,
                'mounted': os.path.exists(DATA_PATH) and os.access(DATA_PATH, os.R_OK)
            },
#Checks if it is readable (os.access(PATH, os.R_OK)).
# Stores this information in a dictionary under the volumes key.

            'config': {
                'path': CONFIG_PATH,
                'mounted': os.path.exists(CONFIG_PATH) and os.access(CONFIG_PATH, os.R_OK)
            },
            'logs': {
                'path': LOG_PATH,
                'mounted': os.path.exists(LOG_PATH) and os.access(LOG_PATH, os.R_OK)
            }
        },
        'timestamp': datetime.datetime.now().isoformat()
    })

@app.route('/api/health')
def health_check():
    """Health check endpoint for Kubernetes liveness and readiness probes"""
    # Check if we can access our mounted volumes
    data_ok = os.path.exists(DATA_PATH) and os.access(DATA_PATH, os.R_OK)
    config_ok = os.path.exists(CONFIG_PATH) and os.access(CONFIG_PATH, os.R_OK)
    logs_ok = os.path.exists(LOG_PATH) and os.access(LOG_PATH, os.W_OK)
    
    # For a real application, you might check database connections, 
    # cache availability, etc.
    
    # Overall health status
    is_healthy = data_ok and config_ok and logs_ok
    
    # Log health check results
    logger.info(f"Health check: {'PASS' if is_healthy else 'FAIL'}")
    
    response = {
        'status': 'healthy' if is_healthy else 'unhealthy',
        'checks': {
            'data_volume': 'accessible' if data_ok else 'inaccessible',
            'config_volume': 'accessible' if config_ok else 'inaccessible',
            'logs_volume': 'writable' if logs_ok else 'not writable'
        },
        'timestamp': datetime.datetime.now().isoformat(),
        'hostname': socket.gethostname()
    }
    
    # Set the HTTP status code based on health
    status_code = 200 if is_healthy else 503
    
    return jsonify(response), status_code

@app.route('/api/metrics')
def get_metrics():
    """API endpoint for application metrics - useful for monitoring systems"""
    # Get basic resource usage stats
    cpu_percent = psutil.cpu_percent()
    memory_info = psutil.virtual_memory()
    disk_info = psutil.disk_usage('/')
    
    # Collect all metrics
    all_metrics = {
        'system': {
            'cpu_percent': cpu_percent,
            'memory_used_percent': memory_info.percent,
            'memory_used_mb': memory_info.used / (1024 * 1024),
            'memory_total_mb': memory_info.total / (1024 * 1024),
            'disk_used_percent': disk_info.percent,
            'disk_used_gb': disk_info.used / (1024**3),
            'disk_total_gb': disk_info.total / (1024**3)
        },
        'application': {
            'uptime_seconds': time.time() - start_time,
            'total_requests': metrics['requests'],
            'data_reads': metrics['data_reads'],
            'data_writes': metrics['data_writes'],
            'errors': metrics['errors']
        },
        'instance': {
            'id': INSTANCE_ID,
            'hostname': socket.gethostname()
        },
        'timestamp': datetime.datetime.now().isoformat()
    }
    
    # Log metrics collection for demonstration
    logger.debug(f"Metrics collected: CPU: {cpu_percent}%, Memory: {memory_info.percent}%")
    
    return jsonify(all_metrics)

# For local testing - this won't run in Kubernetes
if __name__ == '__main__':
    print(f"Starting {APP_NAME} v{APP_VERSION} in {ENVIRONMENT} mode")
    app.run(host='0.0.0.0', port=5000, debug=True)
