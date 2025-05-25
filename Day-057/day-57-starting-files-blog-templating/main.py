from flask import Flask, render_template
import requests


app = Flask(__name__)
data = requests.get("https://api.npoint.io/c790b4d5cab58020d391").json()


@app.route('/')
def home():
    return render_template("index.html", all_posts=data)


@app.route('/post/<int:index>')
def show_post(index):
    for posts in data:
        if posts['id'] == index:
            return render_template("post.html", post=posts)


if __name__ == "__main__":
    app.run(debug=True)