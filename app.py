from Flask import Flask, request, redirect, url_for, render_template_string
from manager import TaskManager

app = Flask(__name__)
manager = TaskManager()

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Task Manager</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 800px; margin: 40px auto; padding: 20px; background: #f5f5f5; }
        h1 { color: #333; border-bottom: 3px solid #4CAF50; padding-bottom: 10px; }
        .form-section { background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); margin-bottom: 20px; }
        input[type="text"], select { width: 100%; padding: 10px; margin: 5px 0 15px; border: 1px solid #ddd; border-radius: 4px; box-sizing: border-box; }
        button { background: #4CAF50; color: white; padding: 10px 20px; border: none; border-radius: 4px; cursor: pointer; font-size: 16px; }
        button:hover { background: #45a049; }
        .filters { margin: 15px 0; }
        .filters a { margin-right: 15px; text-decoration: none; color: #2196F3; font-weight: bold; }
        .filters a.active { color: #333; text-decoration: underline; }
        ul { list-style: none; padding: 0; }
        li { background: white; padding: 12px 15px; margin-bottom: 10px; border-radius: 6px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); display: flex; align-items: center; justify-content: space-between; }
        .task-info { flex: 1; }
        .task-title { font-weight: bold; margin-right: 10px; }
        .task-desc { color: #666; font-size: 0.9em; margin-left: 5px; }
        .task-actions a { margin-left: 10px; text-decoration: none; color: #fff; padding: 4px 10px; border-radius: 4px; font-size: 0.8em; }
        .complete-btn { background: #4CAF50; }
        .delete-btn { background: #f44336; }
        .priority-high { color: #d32f2f; }
        .priority-medium { color: #f9a825; }
        .priority-low { color: #388e3c; }
        .badge { display: inline-block; padding: 2px 8px; border-radius: 12px; color: white; font-size: 0.7em; margin-left: 5px; }
        .badge-high { background: #d32f2f; }
        .badge-medium { background: #f9a825; }
        .badge-low { background: #388e3c; }
    </style>
</head>
<body>
    <h1>📋 Task Manager</h1>

    <!-- Add Task Form -->
    <div class="form-section">
        <form action="/add" method="post">
            <input type="text" name="title" placeholder="Task title" required>
            <input type="text" name="description" placeholder="Description (optional)">
            <select name="priority">
                <option value="">No priority (standard)</option>
                <option value="high">🔴 High</option>
                <option value="medium" selected>🟡 Medium</option>
                <option value="low">🟢 Low</option>
            </select>
            <button type="submit">Add Task</button>
        </form>
    </div>

    <!-- Filter Links -->
    <div class="filters">
        <a href="/?filter=all" class="{% if filter == 'all' %}active{% endif %}">All</a>
        <a href="/?filter=pending" class="{% if filter == 'pending' %}active{% endif %}">Pending</a>
        <a href="/?filter=completed" class="{% if filter == 'completed' %}active{% endif %}">Completed</a>
    </div>

    <!-- Task List -->
    <ul>
    {% for task in tasks %}
        <li>
            <div class="task-info">
                <span class="task-title">
                    {% if task.completed %}✅{% else %}⏳{% endif %}
                    {{ task.title }}
                </span>
                {% if task.description %}
                <span class="task-desc">({{ task.description }})</span>
                {% endif %}
                {% if task.priority %}
                <span class="badge badge-{{ task.priority }}">{{ task.priority }}</span>
                {% endif %}
            </div>
            <div class="task-actions">
                {% if not task.completed %}
                <a href="/complete/{{ task.id }}" class="complete-btn">✔ Complete</a>
                {% endif %}
                <a href="/delete/{{ task.id }}" class="delete-btn">🗑 Delete</a>
            </div>
        </li>
    {% endfor %}
    </ul>
</body>
</html>
"""

@app.route('/')
def index():
    # Get filter from query string
    filter_type = request.args.get('filter', 'all')
    all_tasks = manager.list_tasks(show_all=True)
    
    if filter_type == 'pending':
        tasks = [t for t in all_tasks if not t.completed]
    elif filter_type == 'completed':
        tasks = [t for t in all_tasks if t.completed]
    else:
        tasks = all_tasks
    
    return render_template_string(HTML, tasks=tasks, filter=filter_type)

@app.route('/add', methods=['POST'])
def add():
    title = request.form['title']
    desc = request.form.get('description', '')
    priority = request.form.get('priority', '')
    
    if priority and priority in ['high', 'medium', 'low']:
        manager.add_priority_task(title, priority, desc)
    else:
        manager.add_task(title, desc)
    
    return redirect(url_for('index'))

@app.route('/complete/<int:task_id>')
def complete(task_id):
    manager.complete_task(task_id)
    return redirect(url_for('index'))

@app.route('/delete/<int:task_id>')
def delete(task_id):
    manager.delete_task(task_id)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)