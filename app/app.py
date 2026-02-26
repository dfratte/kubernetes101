"""
Simple Python web application for Kubernetes 101 tutorial
Serves a basic HTML page with Hello World message
"""

from flask import Flask, render_template
import os
import socket
import sys

app = Flask(__name__)

@app.route('/')
def hello():
    """Main route - serves the hello world page"""
    # Get container/pod information
    hostname = socket.gethostname()
    pod_ip = socket.gethostbyname(hostname)
    version = os.environ.get('APP_VERSION', '1.0.0')
    python_version = f"{sys.version_info.major}.{sys.version_info.minor}"

    return render_template(
        'index.html',
        hostname=hostname,
        pod_ip=pod_ip,
        version=version,
        python_version=python_version
    )

@app.route('/health')
def health():
    """Health check endpoint"""
    return {'status': 'healthy', 'app': 'hello-world'}, 200

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port, debug=False)
