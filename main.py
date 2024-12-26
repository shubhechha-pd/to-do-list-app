from flask import Flask, render_template_string, request, redirect, url_for

app = Flask(__name__)

# Temporary storage for tasks (divided into categories)
tasks_today = []
tasks_tomorrow = []
tasks_upcoming = []


@app.route('/')
def home():
    return render_template_string('''
        <html>
            <head>
            <title>To-do List App</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    margin: 20px;
                    background-color: #f4f4f4;
                }
                h1, h2{
                    color: #333;
                }
                ul {
                    list-style-type: none;
                    padding: 0;
                }
                li {
                    background: #fff;
                    margin: 10px 0;
                    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
                    padding: 8px;
                    width: 300px;
                    margin-right: 10px;
                    border: 1px solid #ccc;
                    border-radius: 4px;
                }
                .completed {
                    text-decoration: line-through;
                    color: grey;
                }
                form {
                    margin-top: 20px;
                    
                }
                input[type="text"] {
                    padding: 8px;
                    width: 200px;
                    margin-right: 10px;
                    border: 1px solid #ccc;
                    border-radius: 4px;
                }
                button {
                    padding: 8px 16px;
                    background-color: #008B8B;
                    color: white;
                    border: none;
                    border-radius: 4px;
                    cursor: pointer;
                }
                button:hover {
                    background-color: #008080;
                }
            </style>
            </head>
            <body>
                <h1>To-do List</h1>

                <h2>Today</h2>
                <ul> 
                    {% for task in tasks_today %}
                        <li class="{% if task['completed'] %}completed{% endif %}">
                            <form action="{{ url_for('toggle_completed', task_name=task['name'], category='today') }}" method="post" style="display:inline;">
                                <input type="checkbox" name="completed" {% if task['completed'] %}checked{% endif %} onclick="this.form.submit()"> 
                            </form>
                            {{ loop.index }}. {{ task['name'] }} 
                        </li>
                    {% endfor %}
                </ul>
                <form action="/add/today" method="post">
                    <input type="text" name="task" placeholder="Enter your task" required>
                    <button type="submit">Add Task</button>
                </form>

                <h2>Tomorrow</h2>
                <ul> 
                    {% for task in tasks_tomorrow %}
                        <li class="{% if task['completed'] %}completed{% endif %}">
                            <form action="{{ url_for('toggle_completed', task_name=task['name'], category='tomorrow') }}" method="post" style="display:inline;">
                                <input type="checkbox" name="completed" {% if task['completed'] %}checked{% endif %} onclick="this.form.submit()"> 
                            </form>
                            {{ loop.index }}. {{ task['name'] }} 
                        </li>
                    {% endfor %}
                </ul>
                <form action="/add/tomorrow" method="post">
                    <input type="text" name="task" placeholder="Enter your task" required>
                    <button type="submit">Add Task</button>
                </form>

                <h2>Upcoming</h2>
                <ul> 
                    {% for task in tasks_upcoming %}
                        <li class="{% if task['completed'] %}completed{% endif %}">
                            <form action="{{ url_for('toggle_completed', task_name=task['name'], category='upcoming') }}" method="post" style="display:inline;">
                                <input type="checkbox" name="completed" {% if task['completed'] %}checked{% endif %} onclick="this.form.submit()"> 
                            </form>
                            {{ loop.index }}. {{ task['name'] }} 
                        </li>
                    {% endfor %}
                </ul>
                <form action="/add/upcoming" method="post">
                    <input type="text" name="task" placeholder="Enter your task" required>
                    <button type="submit">Add Task</button>
                </form>
            </body>
        </html>
    ''', tasks_today=tasks_today, tasks_tomorrow=tasks_tomorrow, tasks_upcoming=tasks_upcoming)


# Route to add a new task
@app.route('/add/<category>', methods=['POST'])
def add_task(category):
    task_name = request.form['task']
    task = {'name': task_name, 'completed': False}

    if category == 'today':
        tasks_today.append(task)
    elif category == 'tomorrow':
        tasks_tomorrow.append(task)
    elif category == 'upcoming':
        tasks_upcoming.append(task)

    return redirect(url_for('home'))


# Route to toggle the completion status of a task
@app.route('/toggle_completed/<task_name>/<category>', methods=['POST'])
def toggle_completed(task_name, category):
    # Find the task and toggle its completion status
    if category == 'today':
        task_list = tasks_today
    elif category == 'tomorrow':
        task_list = tasks_tomorrow
    elif category == 'upcoming':
        task_list = tasks_upcoming

    for task in task_list:
        if task['name'] == task_name:
            task['completed'] = not task['completed']  # Toggle completion status

    return redirect(url_for('home'))


if __name__ == "__main__":
    app.run(debug=True)
