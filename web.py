from flask import Flask, redirect, url_for, render_template, request, flash, Markup
import questions
import gunicorn

app = Flask(__name__)

name = ""
domain = "https://aircards.herokuapp.com"
question = ""

@app.route("/", methods=["POST", "GET"])
def home():
    if request.method == "POST":
        name: str = request.form["userInput"]
        question = str(questions.get_question())
        link = f"{domain}/question/{name}/{question}"
        return render_template("start.html", question=question, link=link)
    else:
        return render_template("index.html")

@app.route("/question/<name>/<question>", methods=["POST", "GET"])
def question(name, question):
    if request.method == "POST":
        # question = question[:-1] # remove question mark
        userInput: str = request.form["userInput"]
        link = f"{domain}/response/{name}/{question}/{userInput}"
        return render_template("send-answer.html", name=name, link=link)
    else:
        return render_template("question.html", name=name, question=question)

@app.route("/response/<name>/<question>/<response>/") # passes parameter to variable
def response(name, question, response):
    return render_template("response.html", name=name, question=question, response=response)

@app.route("/<url>/")
def notFound(url):
    return redirect(url_for("home")) # redirects to home

if __name__ == "__main__":
    app.run(debug=True)

# reference: https://www.youtube.com/watch?v=mqhxxeeTbu0