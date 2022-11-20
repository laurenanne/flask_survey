from flask import Flask, request, render_template, redirect, flash
from flask_debugtoolbar import DebugToolbarExtension
from surveys import *

app = Flask(__name__)
app.config['SECRET_KEY'] = "secret"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

responses = []


@app.route('/')
def index():
    """Return homepage"""
    survey_title = satisfaction_survey.title
    survey_inst = satisfaction_survey.instructions
    return render_template("start.html", title=survey_title, instructions=survey_inst)


q = 0


@app.route('/question/<int:q>')
def survey_ques(q):
    """Starts with first question and continues"""
    questions_lst = []
    choices_lst = []

    for item in satisfaction_survey.questions:
        questions_lst.append(item.question)
        choices_lst.append(item.choices)

    if len(responses) == len(satisfaction_survey.questions):
        return redirect('/thanks')
    if len(responses) != q:
        flash("Accessing an invalid question")
        return redirect(f'/question/{len(responses)}')

    ques = questions_lst[q]
    choice = choices_lst[q]
    return render_template("ques.html", question=ques, choice=choice)


@app.route('/answer', methods=["POST"])
def survey_ans():
    """handles the users answers"""
    answer = request.form['ans']
    responses.append(answer)
    """redirects to the next question"""

    while len(responses) < len(satisfaction_survey.questions):
        return redirect(f'/question/{len(responses)}')
    return redirect('/thanks')


@app.route('/thanks')
def thank_you():
    return render_template("thanks.html")
