from flask import Flask, render_template_string

app = Flask(__name__)

# Test Database of users
users = {
    1: "User 1",
    2: "User 2",
    3: "User 3",
    6: "User 6"
}

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
    name = users.get(uid, "")  # If ID doesn't exist -> name is empty ""

    return render_template_string(HTML_TEMPLATE, name=name, uid=uid)


if __name__ == '__main__':
    print("Server is running on http://127.0.0.1:5000/story.php?person=1")
    app.run(port=5000)
