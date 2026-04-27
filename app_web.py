
from flask import Flask, render_template, request, redirect, url_for, session
from ai_generator import AIGenerator
from pdf_handler import PDFHandler
import os

app = Flask(__name__)
app.secret_key = "secret_key"

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        topic = request.form.get("topic")
        file = request.files.get("pdf")

        if topic:
            questions = AIGenerator.generate_questions(topic)
            session["questions"] = questions
            return redirect(url_for("quiz"))

        if file and file.filename.endswith(".pdf"):
            path = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(path)
            content = PDFHandler.read_pdf(path)
            questions = AIGenerator.generate_questions(content)
            session["questions"] = questions
            return redirect(url_for("quiz"))

    return render_template("index.html")


@app.route("/quiz", methods=["GET", "POST"])
def quiz():
    questions = session.get("questions", [])

    if request.method == "POST":
        score = 0
        answers = []

        for i, q in enumerate(questions):
            user_ans = request.form.get(f"q{i}")
            correct = q["answer"]
            if user_ans == correct:
                score += 1
            answers.append((q, user_ans))

        return render_template("result.html",
                               score=score,
                               total=len(questions),
                               answers=answers)

    return render_template("quiz.html", questions=questions)
