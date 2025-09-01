# File Location: labs/lab_03_image_optimization/app.py

from flask import Flask, jsonify
import os
import datetime
import socket
import psutil

app = Flask(__name__)

@app.route('/')
def hello():
    """Main endpoint"""
    return jsonify({
        'message': 'Docker Image Optimization Demo',
        'hostname': socket.gethostname(),
        'timestamp': datetime.datetime.now().isoformat(),
        'python_version': f"{os.sys.version_info.major}.{os.sys.version_info.minor}.{os.sys.version_info.micro}",
        'status': 'success'
    })

@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.datetime.now().isoformat(),
        'service': 'image-optimization-demo'
    }), 200

@app.route('/metrics')
def metrics():
    """System metrics endpoint"""
    try:
        memory = psutil.virtual_memory()
        cpu_percent = psutil.cpu_percent()
        disk = psutil.disk_usage('/')
        
        return jsonify({
            'memory': {
                'total_mb': round(memory.total / 1024 / 1024, 2),
                'used_mb': round(memory.used / 1024 / 1024, 2),
                'percent': memory.percent
            },
            'cpu_percent': cpu_percent,
            'disk': {
                'total_gb': round(disk.total / 1024 / 1024 / 1024, 2),
                'used_gb': round(disk.used / 1024 / 1024 / 1024, 2),
                'percent': round((disk.used / disk.total) * 100, 2)
            },
            'timestamp': datetime.datetime.now().isoformat()
        })
    except ImportError:
        return jsonify({
            'message': 'psutil not available - minimal image',
            'timestamp': datetime.datetime.now().isoformat()
        })

@app.route('/info')
def info():
    """Container information"""
    return jsonify({
        'container_info': {
            'hostname': socket.gethostname(),
            'platform': os.sys.platform,
            'python_version': os.sys.version,
            'environment_variables': {
                key: value for key, value in os.environ.items() 
                if not any(secret in key.upper() for secret in ['PASSWORD', 'SECRET', 'TOKEN', 'KEY'])
            }
        },
        'timestamp': datetime.datetime.now().isoformat()
    })

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('FLASK_ENV') == 'development'
    
    print(f"Starting Flask application on port {port}")
    print(f"Debug mode: {debug}")
    
    app.run(host='0.0.0.0', port=port, debug=debug)