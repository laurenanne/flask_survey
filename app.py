from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import *


app = Flask(__name__)
app.config['SECRET_KEY'] = "secret"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)
response_key = "responses"


@app.route('/')
def index():
    """Return homepage where survey start button resides"""
    survey_title = satisfaction_survey.title
    survey_inst = satisfaction_survey.instructions
    return render_template("start.html", title=survey_title, instructions=survey_inst)

@app.route('/start')
def start():
    """resets the session key and directs to the first question"""
    session[response_key] = []
    ques =satisfaction_survey.questions[0].question
    choice = satisfaction_survey.questions[0].choices
    return render_template("ques0.html", question=ques, choice=choice)
    

@app.route('/answer', methods=["POST"])
def survey_ans():
    """handles the users answers"""
    answer = request.form['ans']

    responses = session[response_key]
    responses.append(answer)
    session[response_key] = responses
    
    """redirects to the next question"""
    while len(responses) < len(satisfaction_survey.questions):
        return redirect(f'/question/{len(responses)}')
    return redirect('/thanks')



@app.route('/question/<int:q>')
def survey_ques(q):
    """Starts with first question and continues"""
    responses = session.get(response_key)

    if len(responses) == len(satisfaction_survey.questions):
     return redirect('/thanks')
    if len(responses) != q:
        flash("Accessing an invalid question")
        return redirect(f'/question/{len(responses)}')

    ques = satisfaction_survey.questions[q].question
    choice = satisfaction_survey.questions[q].choices
    return render_template("ques.html", question=ques, choice=choice)



@app.route('/thanks')
def thank_you():
    return render_template("thanks.html")
   