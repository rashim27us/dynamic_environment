import requests
import os
import time
import json
from typing import Dict, Any

class VMAnalyzer:
    def __init__(self, vm_ip: str, vm_port: int):
        self.base_url = f"http://{vm_ip}:{vm_port}"
    
    def upload_executable(self, file_path: str) -> Dict[str, Any]:
        with open(file_path, 'rb') as f:
            files = {'file': f}
            response = requests.post(f"{self.base_url}/upload_executable", files=files)
        
        # Check if the response contains valid JSON
        try:
            return response
        except requests.exceptions.JSONDecodeError:
            print("Error: Response is not in JSON format")
            print("Response content:", response.text)
            return {"error": "Invalid JSON response"}
    
    def get_process_info(self, process_name: str) -> Dict[str, Any]:
        data = {'process_name': process_name}
        response = requests.post(f"{self.base_url}/process_info", json=data)
        return response
        # return response.json()
    
    def monitor_process(self, process_name: str, duration_seconds: int = 60, interval: int = 1):
        """Monitor a process for a specified duration, collecting data at regular intervals"""
        monitoring_data = []
        
        for _ in range(0, duration_seconds, interval):
            process_info = self.get_process_info(process_name)
            monitoring_data.append(process_info)
            time.sleep(interval)
        
        return monitoring_data

# Example usage
if __name__ == "__main__":
    analyzer = VMAnalyzer("192.168.56.101", 5000)
    
    # Upload executable
    result = analyzer.upload_executable("/home/yash-rastogi/Documents/cyberWattDefenderAI/malware/malware/downloads/0fd8b2570b5b38cb65325116d2ea01d414876f903cf72c26a1733a1d6f35bd22.exe")
    print("Upload result:", result)
    
    # Monitor process
    data = analyzer.monitor_process("0b2957e10a9d6c29a680e112571ea46be5fedeac0ecc6f0097337f40d61a4cb1.exe", duration_seconds=300)
    
    # Save results
    with open("analysis_results.json", "w") as f:
        json.dump(data, f, indent=4)