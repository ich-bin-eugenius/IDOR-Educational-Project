from flask import Flask, render_template_string
import random

app = Flask(__name__)


names = ["Tom", "Bob", "Steve", "King", "Lord", "Voldemort", "Harry", "Roan", "Allison", "Luke", "Paul", "James"]
second_names = ["Green", "White", "Mclaren", "Black", "Burgers", "Rowling", "Dvorak", "Havel", "Joska", "Czerny"]

# Test Database of users
users = {1: "admin"}

id_person = 2

for _ in range(10000):
    full_name = f"{random.choice(names)} {random.choice(second_names)}"
    users[id_person] = full_name
    id_person += 1

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head><title>Profile</title></head>
<body>
    <div class="container">
        <li style="float:right;" title="Student: {{ name }}">
            <svg>...</svg>
            <span style="margin-left:2px;">{{ name }}</span>
        </li>
    </div>
    <h1>Welcome</h1>
    <p>User's ID: {{ uid }}</p>
</body>
</html>
"""


@app.route('/story.php')
def profile():
    import flask
    uid = flask.request.args.get('person', type=int)

    # Vulnerability: No verification, just print the name if it exists
    name = users.get(uid, "")  # If ID doesn't exist -> name is empty " "

    return render_template_string(HTML_TEMPLATE, name=name, uid=uid)


if __name__ == '__main__':
    print("Server is running on http://127.0.0.1:5000/story.php?person=1")
    app.run(port=5000)
