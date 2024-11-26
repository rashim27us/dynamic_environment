from flask import Flask, request, jsonify
import psutil
import win32process
import win32gui
import win32con
import os
import json

app = Flask(__name__)

@app.route('/process_info', methods=['POST'])
def get_process_info():
    data = request.json()
    process_name = data.get('process_name')
    
    process_info = {}
    for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent', 'connections']):
        try:
            if proc.info['name'] == process_name:
                process_info = {
                    'pid': proc.info['pid'],
                    'cpu_usage': proc.info['cpu_percent'],
                    'memory_usage': proc.info['memory_percent'],
                    'network_connections': [conn._asdict() for conn in proc.info['connections']],
                    'open_handles': len(proc.open_files()),
                    'threads': len(proc.threads()),
                    'child_processes': [child.pid for child in proc.children()]
                }
                break
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    
    return jsonify(process_info)

@app.route('/upload_executable', methods=['POST'])
def upload_executable():
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No filename provided'}), 400
    
    save_path = os.path.join('C:\\analysis', file.filename)
    file.save(save_path)
    return jsonify({'message': 'File uploaded successfully', 'path': save_path})

if __name__ == '__main__':
    app.run(host='192.168.56.101', port=5000)