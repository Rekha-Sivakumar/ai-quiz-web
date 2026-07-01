from flask import Flask, render_template, request, redirect, url_for, session, flash
from ai_generator import AIGenerator
from pdf_handler import PDFHandler
import os

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "dev-secret-key-change-me")

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        topic = request.form.get("topic", "").strip()
        file = request.files.get("pdf")

        if topic:
            questions = AIGenerator.generate_questions(topic)
            if not questions:
                flash("Couldn't generate questions for that topic. Please try again.")
                return redirect(url_for("index"))
            session["questions"] = questions
            return redirect(url_for("quiz"))

        if file and file.filename and file.filename.endswith(".pdf"):
            path = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(path)
            content = PDFHandler.read_pdf(path)
            if not content:
                flash("Couldn't read any text from that PDF. Please try another file.")
                return redirect(url_for("index"))
            questions = AIGenerator.generate_questions(content)
            if not questions:
                flash("Couldn't generate questions from that PDF. Please try again.")
                return redirect(url_for("index"))
            session["questions"] = questions
            return redirect(url_for("quiz"))

        flash("Please enter a topic or upload a PDF.")
        return redirect(url_for("index"))

    return render_template("index.html")


@app.route("/quiz", methods=["GET", "POST"])
def quiz():
    questions = session.get("questions", [])

    if not questions:
        flash("Your quiz session expired or no quiz was generated yet. Please start again.")
        return redirect(url_for("index"))

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
