from flask import Flask, render_template, request, jsonify
import os
from openai import OpenAI

# ==============================
# OpenAI Client (Secure)
# ==============================
api_key = os.getenv("")

client = OpenAI(api_key=api_key) if api_key else None

# ==============================
# Import Converters
# ==============================
from converter.c.to_python import convert as c_to_python
from converter.c.to_java import convert as c_to_java
from converter.c.to_cpp import convert as c_to_cpp

from converter.cpp.to_c import convert as cpp_to_c
from converter.cpp.to_java import convert as cpp_to_java
from converter.cpp.to_python import convert as cpp_to_python

from converter.java.to_c import convert as java_to_c
from converter.java.to_cpp import convert as java_to_cpp
from converter.java.to_python import convert as java_to_python

from converter.python.to_c import convert as python_to_c
from converter.python.to_cpp import convert as python_to_cpp
from converter.python.to_java import convert as python_to_java


# ==============================
# Flask App
# ==============================
app = Flask(__name__)


# ==============================
# Converter Dispatcher
# ==============================
CONVERTERS = {
    ("c", "python"): c_to_python,
    ("c", "java"): c_to_java,
    ("c", "cpp"): c_to_cpp,

    ("cpp", "c"): cpp_to_c,
    ("cpp", "java"): cpp_to_java,
    ("cpp", "python"): cpp_to_python,

    ("java", "c"): java_to_c,
    ("java", "cpp"): java_to_cpp,
    ("java", "python"): java_to_python,

    ("python", "c"): python_to_c,
    ("python", "cpp"): python_to_cpp,
    ("python", "java"): python_to_java,
}


# ==============================
# AI Analyzer
# ==============================


def ai_analyze(code, source, target):


    if client is None:
        return """
Explanation:
AI analysis unavailable.

Warnings:
No OpenAI API key configured.

Complexity:
Time Complexity: Unknown
Space Complexity: Unknown

Syntax Mapping:
Basic syntax conversion.
"""

    prompt = f"""
You are an expert programming tutor and static code analyzer.

Analyze this {source} code that will be converted to {target}.

Provide:

1. Explanation of what the code does (clear and student-friendly).
2. Any warnings or potential issues (if none, say "No issues detected.").
3. Time complexity.
4. Space complexity.
5. Key syntax differences between {source} and {target}.

Code:
{code}

Respond STRICTLY in this format:

Explanation:
<text>

Warnings:
<text>

Complexity:
<text>

Syntax Mapping:
<text>
"""
    prompt = f"""
You are an expert programming tutor and static code analyzer.

Analyze this {source} code that will be converted to {target}.

Provide:

1. Explanation of what the code does (clear and student-friendly).
2. Any warnings or potential issues (if none, say "No issues detected.").
3. Time complexity.
4. Space complexity.
5. Key syntax differences between {source} and {target}.

Code:
{code}

Respond STRICTLY in this format:

Explanation:
<text>

Warnings:
<text>

Complexity:
<text>

Syntax Mapping:
<text>
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2
    )

    return response.choices[0].message.content


# ==============================
# Parse AI Response
# ==============================
def parse_ai_response(text):

    sections = {
        "explanation": "",
        "warnings": "",
        "complexity": "",
        "syntax_mapping": ""
    }

    current = None

    for line in text.split("\n"):

        line = line.strip()

        if line.startswith("Explanation:"):
            current = "explanation"
            continue
        elif line.startswith("Warnings:"):
            current = "warnings"
            continue
        elif line.startswith("Complexity:"):
            current = "complexity"
            continue
        elif line.startswith("Syntax Mapping:"):
            current = "syntax_mapping"
            continue

        if current:
            sections[current] += line + "\n"

    return sections


# ==============================
# Routes
# ==============================
@app.route("/")
def home():
    return render_template("index.html")


@app.route("/api/convert", methods=["POST"])
def convert_api():

    try:
        data = request.get_json()

        code = data.get("code", "")
        source = data.get("source", "")
        target = data.get("target", "")

        # Basic Validation
        if not code.strip():
            return jsonify({
                "converted": "",
                "syntax_mapping": "",
                "explanation": "",
                "warnings": "No code provided.",
                "complexity": ""
            })

        if source == target:
            return jsonify({
                "converted": "",
                "syntax_mapping": "",
                "explanation": "",
                "warnings": "Source and target languages must be different.",
                "complexity": ""
            })

        converter_function = CONVERTERS.get((source, target))

        if not converter_function:
            return jsonify({
                "converted": "",
                "syntax_mapping": "",
                "explanation": "",
                "warnings": "Conversion not supported yet.",
                "complexity": ""
            })

        # Run converter safely
        try:
            converted_code = converter_function(code)
        except Exception as e:
            return jsonify({
                "converted": "",
                "syntax_mapping": "",
                "explanation": "",
                "warnings": f"Conversion error: {str(e)}",
                "complexity": ""
            })

        # ======================
        # AI Analysis Section
        # ======================
        try:
            analysis_text = ai_analyze(code, source, target)
            sections = parse_ai_response(analysis_text)
        except Exception as e:
            return jsonify({
                "converted": converted_code,
                "syntax_mapping": "",
                "explanation": "",
                "warnings": f"AI analysis error: {str(e)}",
                "complexity": ""
            })

        return jsonify({
            "converted": converted_code,
            "syntax_mapping": sections["syntax_mapping"],
            "explanation": sections["explanation"],
            "warnings": sections["warnings"],
            "complexity": sections["complexity"]
        })

    except Exception as e:
        return jsonify({
            "converted": "",
            "syntax_mapping": "",
            "explanation": "",
            "warnings": f"Server error: {str(e)}",
            "complexity": ""
        })


# ==============================
# Run App
# ==============================
if __name__ == "__main__":
    app.run(debug=True, port=5001)