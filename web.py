from flask import Flask, redirect, url_for, render_template, request
import questions
import url

app = Flask(__name__)

name = "someone"
domain = "https://aircards.herokuapp.com"
question = ""
message = ""
message_link = ""

@app.route("/")
def home():
        return render_template("index.html")

@app.route("/cards/", methods=["POST", "GET"])
def cards():
    if request.method == "POST":
        name: str = request.form["userInput"]
        question = str(questions.get_question())
        name = url.toUrl(name)
        question = url.toUrl(question)
        link = f"{domain}/question/{name}/{question}"
        return render_template("start.html", question=url.toString(question), link=link)
    else:
        return render_template("cards.html")

# basic flask framework reference: https://www.youtube.com/watch?v=mqhxxeeTbu0

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

# 1. Person A: get first message (of person A)

@app.route("/message/initial/", methods=["POST", "GET"])
def initial_message():
    if request.method == "POST":
        message: str = request.form["userInput"]
        message = url.toUrl(message)
        return redirect(f"/message/name/{message}/")
    return render_template("message.html")

# 2. Person A: get name (of person A)

@app.route("/message/name/<message>/", methods=["POST", "GET"])
def name_a(message):
    if request.method == "POST":
        name: str = request.form["userInput"]
        name = url.toUrl(name)
        message_link = f"{domain}/message/inbox/initial/{name}/{message}/"
        return render_template("send-initial-message.html", message_link=message_link)
    return render_template("name.html")

# 3. Person B: receive first message (of person A), get answer (of person B)

@app.route("/message/inbox/initial/<name_a>/<message>/", methods=["POST", "GET"])
def initial_inbox(name_a, message):
    if request.method == "POST":
        answer: str = request.form["userInput"]
        answer = url.toUrl(answer)
        return redirect(f"/message/b/{name_a}/name/{message}/{answer}/")
    return render_template("initial-inbox.html", name=url.toString(name_a), message=url.toString(message))

# 4. Person B: get name (of person B)

@app.route("/message/b/<name_a>/name/<message>/<answer>/", methods=["POST", "GET"])
def name_b(name_a, message, answer):
    if request.method == "POST":
        name_b: str = request.form["userInput"]
        name_b = url.toUrl(name_b)
        message_link = f"{domain}/message/inbox/a/{name_a}/{name_b}/{message}/{answer}/"
        return render_template("send-message.html", name=url.toString(name_a), message_link=message_link)
    return render_template("name-b.html", name=url.toString(name_a), message=url.toString(message))

# 4. Person A: receive previous answer (of person B), send new message (to person B)

@app.route("/message/inbox/a/<name_a>/<name_b>/<previous>/<message>/", methods=["POST", "GET"])
def inbox_a(name_a, name_b, message, previous):
    if request.method == "POST":
        answer: str = request.form["userInput"]
        answer = url.toUrl(answer)
        message = url.toUrl(message)
        message_link = f"{domain}/message/inbox/b/{name_a}/{name_b}/{message}/{answer}"
        return render_template("send-message.html", name=url.toString(name_b), message_link=message_link)
    return render_template("inbox.html", name=url.toString(name_b), message=url.toString(message), previous=url.toString(previous))

# 4. Person B: receive previous answer (of person A), send new message (to person A)

@app.route("/message/inbox/b/<name_a>/<name_b>/<previous>/<message>/", methods=["POST", "GET"])
def inbox_b(name_a, name_b, message, previous):
    if request.method == "POST":
        answer: str = request.form["userInput"]
        answer = url.toUrl(answer)
        message = url.toUrl(message)
        message_link = f"{domain}/message/inbox/a/{name_a}/{name_b}/{message}/{answer}"
        return render_template("send-message.html", name=url.toString(name_a), message_link=message_link)
    return render_template("inbox.html", name=url.toString(name_a), message=url.toString(message), previous=url.toString(previous))

@app.route("/<url>/")
def notFound(url):
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(debug=True)
