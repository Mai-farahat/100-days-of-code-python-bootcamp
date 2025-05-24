from flask import Flask

app = Flask(__name__)


print(__name__)
@app.route("/")
def hello_world():
    return ('<h1 style="text-align: center">Hello, World!</h1>'
            '<p>cute kitten.<p/>'
            '<img src="https://media3.giphy.com/media/v1.Y2lkPTc5MGI3NjExNzVpMmU4OXZkamx0dHg1ZnhvbWlsNG13cDl0cWQ2bzRvOWVtYXFlNiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/5dYbT8yNjS23ZLWzhd/giphy.gif" width="500">')


@app.route("/bye")
@make_bold
def say_bye():
    return "Bye"

#day-55
# @app.route("/username/<name>")
# def greet(name):
#     return f"Hello {name}!"

# @app.route("/username/<path:name>")
# def greet(name):
#     return f"Hello there {name + '12'}!"

@app.route("/username/<name>/<int:number>")
def greet(name, number):
    return f"Hello there {name}, you are {number} years old!"

if __name__ == "__main__":
    app.run(debug=True)