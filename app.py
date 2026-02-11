





from flask import Flask, render_template, request
import pdfplumber
import os

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def generate_summary(text):
    # Simple structured summary without OpenAI
    intro = text[:300]

    summary = f"""
📌 Structured Summary

1️⃣ Introduction:
{intro}...

2️⃣ Key Points:
- This document discusses important academic concepts.
- It contains structured information extracted from the PDF.
- The system processes uploaded files and generates summaries.

3️⃣ Conclusion:
This PDF has been analyzed and summarized in structured format.
"""

    return summary

@app.route("/", methods=["GET", "POST"])
def index():
    summary = ""

    if request.method == "POST":
        if "file" not in request.files:
            return "No file uploaded"

        file = request.files["file"]

        if file.filename == "":
            return "No selected file"

        filepath = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(filepath)

        text = ""

        try:
            with pdfplumber.open(filepath) as pdf:
                for page in pdf.pages:
                    extracted = page.extract_text()
                    if extracted:
                        text += extracted

            if text.strip() == "":
                summary = "⚠ PDF has no readable text."
            else:
                summary = generate_summary(text)

        except Exception as e:
            summary = f"Error reading PDF: {str(e)}"

    return render_template("index.html", summary=summary)

if __name__ == "__main__":
    app.run(debug=True)    