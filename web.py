from flask import Flask, redirect, url_for, render_template, request, flash, Markup
import questions
import gunicorn
import url

app = Flask(__name__)

name = "someone"
domain = "https://aircards.herokuapp.com"
question = ""
message = ""
message_link = ""

@app.route("/", methods=["POST", "GET"])
def home():
    if request.method == "POST":
        name: str = request.form["userInput"]
        question = str(questions.get_question())
        name = url.toUrl(name)
        question = url.toUrl(question)
        link = f"{domain}/question/{name}/{question}"
        return render_template("start.html", question=url.toString(question), link=link)
    else:
        return render_template("index.html")

@app.route("/question/<name>/<question>/", methods=["POST", "GET"])
def question(name, question):
    if request.method == "POST":
        # question = question[:-1] # remove question mark
        userInput: str = request.form["userInput"]
        userInput = url.toUrl(userInput)
        name = url.toUrl(name)
        question = url.toUrl(question)
        link = f"{domain}/response/{name}/{question}/{userInput}"
        return render_template("send-answer.html", name=url.toString(name), link=link)
    else:
        return render_template("question.html", name=url.toString(name), question=url.toString(question))

@app.route("/response/<name>/<question>/<response>/")
def response(name, question, response):
    return render_template("response.html", name=url.toString(name), question=url.toString(question), response=url.toString(response))

@app.route("/message/", methods=["POST", "GET"])
def message():
    if request.method == "POST":
        message: str = request.form["userInput"]
        message = url.toUrl(message)
        message_link = f"{domain}/message/inbox/initial/{message}/"
        return render_template("send-message.html", message_link=message_link)
    return render_template("message.html")

@app.route("/message/inbox/initial/<message>/", methods=["POST", "GET"])
def initial_inbox(message):
    if request.method == "POST":
        answer: str = request.form["userInput"]
        answer = url.toUrl(answer)
        message = url.toUrl(message)
        message_link = f"{domain}/message/inbox/{message}/{answer}"
        return render_template("send-message.html", message_link=message_link)
    return render_template("initial-inbox.html", name=url.toString(name), message=url.toString(message))

@app.route("/message/inbox/<previous>/<message>/", methods=["POST", "GET"])
def inbox(message, previous):
    if request.method == "POST":
        answer: str = request.form["userInput"]
        answer = url.toUrl(answer)
        message = url.toUrl(message)
        message_link = f"{domain}/message/inbox/{message}/{answer}"
        return render_template("send-message.html", message_link=message_link)
    return render_template("inbox.html", name=url.toString(name), message=url.toString(message), previous=url.toString(previous))

@app.route("/<url>/")
def notFound(url):
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(debug=True)

# reference: https://www.youtube.com/watch?v=mqhxxeeTbu0