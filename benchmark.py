import requests
import time
import os

def make_request_with_timeout(url, timeout):
    start_time = time.time()
    while True:
        try:
            response = requests.get(url)
            if response.status_code == 200:
                end_time = time.time()
                print(f"Time taken to get a response: {end_time - start_time:.2f} seconds")
                return response.json()
        except requests.RequestException as e:
            print(f"Request failed: {e}")
        
        if time.time() - start_time > timeout:
            raise TimeoutError("Request timed out after {} seconds".format(timeout))
        time.sleep(1)  # Wait for 1 second before retrying

if __name__ == "__main__":
    endpoint = "http://localhost:9081/api/v1/healthz"
    timeout = 60  # seconds
    try:
        data = make_request_with_timeout(endpoint, timeout)
        print("Received data:", data)
        # Kill any running main.go apps on exit
        # Find the process id of the running main.go app and kill it
        try:
            pid = int(os.popen("pgrep -f /tmp/go-build3249752709/b001/exe/main").read().strip())
            os.kill(pid, 9)
            print(f"Killed process with pid: {pid}")
        except ValueError:
            print("No running main.go process found")
        except OSError as e:
            print(f"Error killing process: {e}")
    except TimeoutError as e:
        print(e)