from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
import os
from analyzer.validator import validate_structure
from analyzer.semantic_ai import analyze_paragraphs
from analyzer.apa_checker import check_apa_citations
from dotenv import load_dotenv
from flask_cors import CORS

load_dotenv()

app = Flask(__name__)
CORS(app)
app.config['UPLOAD_FOLDER'] = 'uploads/'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route("/upload", methods=["POST"])
def upload_essay():
    student_name = request.form.get("name")
    paragraph_count = int(request.form.get("paragraph_count"))
    min_lines = int(request.form.get("min_lines"))
    max_lines = int(request.form.get("max_lines"))
    min_words = int(request.form.get("min_words"))
    max_words = int(request.form.get("max_words"))
    argument_types = request.form.getlist("argument_types")

    file = request.files.get("file")
    if not file:
        return jsonify({"error": "Archivo no encontrado"}), 400

    filename = secure_filename(file.filename)
    path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(path)

    # Validaciones básicas
    structure_results = validate_structure(path, paragraph_count, min_lines, max_lines, min_words, max_words)

    # Análisis semántico con IA (DeepSeek)
    semantic_results = analyze_paragraphs(path, argument_types)

    # Revisión de citas APA
    apa_results = check_apa_citations(path)

    return jsonify({
        "student": student_name,
        "structure_analysis": structure_results,
        "semantic_analysis": semantic_results,
        "apa_check": apa_results
    })

if __name__ == "__main__":
    app.run(debug=True)
