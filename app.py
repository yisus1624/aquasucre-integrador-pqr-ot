import os
from flask import Flask, render_template
import requests

app = Flask(__name__)

FRAPPE_URL = os.environ.get("FRAPPE_URL", "").rstrip("/")
API_KEY = os.environ.get("API_KEY")
API_SECRET = os.environ.get("API_SECRET")

def frappe_get(resource, params=None):
    url = f"{FRAPPE_URL}/api/resource/{resource}"
    headers = {
        "Authorization": f"token {API_KEY}:{API_SECRET}",
        "X-Frappe-Site-Name": "helpdesk.localhost"
    }
    r = requests.get(url, headers=headers, params=params, timeout=30)
    r.raise_for_status()
    return r.json()

@app.route("/")
def index():
    error = None
    tickets = []
    try:
        data = frappe_get("HD Ticket", params={"fields": '["name","subject","status","priority","creation"]'})
        tickets = data.get("data", [])
    except Exception as e:
        error = str(e)
    return render_template("index.html", tickets=tickets, error=error)

@app.route("/ticket/<name>")
def ticket_detail(name):
    error = None
    ticket = {}
    try:
        data = frappe_get(f"HD Ticket/{name}")
        ticket = data.get("data", {})
    except Exception as e:
        error = str(e)
    return render_template("ticket.html", ticket=ticket, error=error)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
