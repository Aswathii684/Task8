from flask import Flask, request, redirect, url_for, render_template_string
import json
import os

app = Flask(__name__)
TASKS_FILE = 'tasks.json'


def load_tasks():
    if not os.path.exists(TASKS_FILE):
        return []
    with open(TASKS_FILE, 'r') as f:
        return json.load(f)


def save_tasks(tasks):
    with open(TASKS_FILE, 'w') as f:
        json.dump(tasks, f)
        
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>To-Do List</title>
    <style>
        body { font-family: Arial; padding: 20px; }
        .completed { text-decoration: line-through; color: gray; }
        li { margin-bottom: 10px; }
    </style>
</head>
<body>
    <h1>📝 My To-Do List</h1>
    <form method="POST" action="/add">
        <input type="text" name="task" placeholder="Add a new task" required>
        <button type="submit">Add</button>
    </form>
    <ul>
        {% for task in tasks %}
        <li>
            <form style="display:inline;" method="POST" action="/toggle/{{ loop.index0 }}">
                <input type="checkbox" onChange="this.form.submit()" {% if task.completed %}checked{% endif %}>
            </form>
            <span class="{% if task.completed %}completed{% endif %}">{{ task.text }}</span>
            <form style="display:inline;" method="POST" action="/delete/{{ loop.index0 }}">
                <button type="submit">❌</button>
            </form>
        </li>
        {% endfor %}
    </ul>
</body>
</html>
'''

@app.route('/')
def index():
    tasks = load_tasks()
    return render_template_string(HTML_TEMPLATE, tasks=tasks)

@app.route('/add', methods=['POST'])
def add():
    task = request.form.get('task')
    tasks = load_tasks()
    tasks.append({'text': task, 'completed': False})
    save_tasks(tasks)
    return redirect(url_for('index'))

@app.route('/delete/<int:task_id>', methods=['POST'])
def delete(task_id):
    tasks = load_tasks()
    if 0 <= task_id < len(tasks):
        tasks.pop(task_id)
        save_tasks(tasks)
    return redirect(url_for('index'))

@app.route('/toggle/<int:task_id>', methods=['POST'])
def toggle(task_id):
    tasks = load_tasks()
    if 0 <= task_id < len(tasks):
        tasks[task_id]['completed'] = not tasks[task_id]['completed']
        save_tasks(tasks)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
