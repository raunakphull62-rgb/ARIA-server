# plugins/aria-docker-tool/main.py
import subprocess
import sys

def docker_start():
    container = input("Container name/ID: ")
    subprocess.run(["docker", "start", container])

def docker_stop():
    container = input("Container name/ID: ")
    subprocess.run(["docker", "stop", container])

def docker_logs_ai():
    container = input("Container name/ID: ")
    logs = subprocess.check_output(["docker", "logs", container, "--tail", "50"]).decode()
    print("Logs:")
    print(logs)
    # In real version, send to AI for explanation
    print("AI would analyze these logs...")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python main.py <docker-start|docker-stop|docker-logs-ai>")
    else:
        cmd = sys.argv[1]
        if cmd == "docker-start":
            docker_start()
        elif cmd == "docker-stop":
            docker_stop()
        elif cmd == "docker-logs-ai":
            docker_logs_ai()
        else:
            print(f"Unknown command: {cmd}")
