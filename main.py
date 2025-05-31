from flask import Flask, jsonify, request

app = Flask(__name__)

# In-memory "database" of tasks
tasks = [
    {"id": 1, "title": "Learn Flask", "done": False},
    {"id": 2, "title": "Build an API", "done": False}
]

# Get all tasks
@app.route('/tasks', methods=['GET'])
def get_tasks():
    return jsonify(tasks)

# Get a specific task
@app.route('/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    task = next((t for t in tasks if t['id'] == task_id), None)
    if task:
        return jsonify(task)
    return jsonify({"error": "Task not found"}), 404

# Create a new task
@app.route('/tasks', methods=['POST'])
def create_task():
    if not request.json or 'title' not in request.json:
        return jsonify({'error': 'Bad request'}), 400
    new_task = {
        "id": tasks[-1]['id'] + 1 if tasks else 1,
        "title": request.json['title'],
        "done": False
    }
    tasks.append(new_task)
    return jsonify(new_task), 201

# Update a task
@app.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    task = next((t for t in tasks if t['id'] == task_id), None)
    if not task:
        return jsonify({'error': 'Task not found'}), 404
    data = request.json
    task['title'] = data.get('title', task['title'])
    task['done'] = data.get('done', task['done'])
    return jsonify(task)

# Delete a task
@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    global tasks
    tasks = [t for t in tasks if t['id'] != task_id]
    return jsonify({'result': 'Task deleted'})

if __name__ == '__main__':
    app.run(debug=True)
