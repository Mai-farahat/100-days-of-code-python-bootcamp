from flask import Flask, render_template, request, jsonify
from datetime import datetime
import uuid

app = Flask(__name__)

# In-memory task store (replace with a database for production)
tasks = [
    {"id": str(uuid.uuid4())[:7], "title": "Design system color palette",    "col": "done",  "priority": "high", "tag": "design", "created": "Mar 4"},
    {"id": str(uuid.uuid4())[:7], "title": "Set up project repo & CI/CD",    "col": "done",  "priority": "high", "tag": "dev",    "created": "Mar 5"},
    {"id": str(uuid.uuid4())[:7], "title": "Build authentication flow",       "col": "doing", "priority": "high", "tag": "dev",    "created": "Mar 6"},
    {"id": str(uuid.uuid4())[:7], "title": "Write API documentation",         "col": "doing", "priority": "med",  "tag": "docs",   "created": "Mar 6"},
    {"id": str(uuid.uuid4())[:7], "title": "Fix navbar scroll bug on mobile", "col": "todo",  "priority": "high", "tag": "bug",    "created": "Mar 7"},
    {"id": str(uuid.uuid4())[:7], "title": "Add dark mode toggle",            "col": "todo",  "priority": "low",  "tag": "feature","created": "Mar 7"},
    {"id": str(uuid.uuid4())[:7], "title": "Review pull request #47",         "col": "todo",  "priority": "med",  "tag": "review", "created": "Mar 7"},
]


# ── Routes ────────────────────────────────────────────────────────────────────

@app.route("/")
def index():
    """Render the main Kanban board."""
    today = datetime.now().strftime("%a, %b %d").replace(" 0", " ")
    counts = {
        "todo":  sum(1 for t in tasks if t["col"] == "todo"),
        "doing": sum(1 for t in tasks if t["col"] == "doing"),
        "done":  sum(1 for t in tasks if t["col"] == "done"),
    }
    total = len(tasks)
    pct = round((counts["done"] / total) * 100) if total > 0 else 0
    return render_template("index.html", tasks=tasks, today=today,
                           counts=counts, total=total, pct=pct)


# ── API ───────────────────────────────────────────────────────────────────────

@app.route("/api/tasks", methods=["GET"])
def get_tasks():
    """Return all tasks as JSON."""
    return jsonify(tasks)


@app.route("/api/tasks", methods=["POST"])
def create_task():
    """Create a new task."""
    data = request.get_json()
    title = (data.get("title") or "").strip()
    if not title:
        return jsonify({"error": "Title is required"}), 400

    task = {
        "id":       str(uuid.uuid4())[:7],
        "title":    title,
        "col":      data.get("col", "todo"),
        "priority": data.get("priority", "med"),
        "tag":      data.get("tag", "other"),
        "created":  datetime.now().strftime("%b %d").replace(" 0", " "),
    }
    tasks.append(task)
    return jsonify(task), 201


@app.route("/api/tasks/<task_id>", methods=["PATCH"])
def update_task(task_id):
    """Move a task to a different column (or update any field)."""
    task = next((t for t in tasks if t["id"] == task_id), None)
    if not task:
        return jsonify({"error": "Task not found"}), 404

    data = request.get_json()
    for field in ("col", "priority", "tag", "title"):
        if field in data:
            task[field] = data[field]

    return jsonify(task)


@app.route("/api/tasks/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    """Delete a task by ID."""
    global tasks
    before = len(tasks)
    tasks = [t for t in tasks if t["id"] != task_id]
    if len(tasks) == before:
        return jsonify({"error": "Task not found"}), 404
    return jsonify({"deleted": task_id})


# ── Run ───────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    app.run(debug=True, port=5000)