import os
from google import genai
from google.genai import types
from docx import Document
from dotenv import load_dotenv

load_dotenv()

GOOGLE_API_KEY = "AIzaSyAHuN-zG7t3RwA1EE_D-gYRvzGKK-slpqE"

client=genai.Client(api_key=GOOGLE_API_KEY)


def prompt_gemini(message: str) -> str:
    try:
     
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            # system_instruction="Actúa como un profesor de redacción. Analiza el párrafo y sugiere mejoras.",
            contents = types.Content(
                role='user',
                parts=[types.Part.from_text(text=message)]
            )
        )

        return response.text
    except Exception as e:
        print("Error al procesar el mensaje:", str(e))
        return f"❌ Error al procesar el párrafo: {str(e)}"

def analyze_paragraphs(path, argument_types):
    doc = Document(path)
    paragraphs = [p.text.strip() for p in doc.paragraphs if p.text.strip()]
    results = []

    for idx, paragraph in enumerate(paragraphs):
        if idx == 0:
            tipo = "introducción"
        elif idx == len(paragraphs) - 1:
            tipo = "conclusión"
        elif idx - 1 < len(argument_types):
            tipo = argument_types[idx - 1]
        else:
            tipo = "argumento no especificado"

        msg = (
            f"Analiza este párrafo como {tipo}. Evalúa si sigue la estructura esperada para ese tipo de argumento, "
            f"señala si hay errores, ambigüedades o falta de claridad. Luego, sugiere mejoras usando conectores, "
            f"palabras clave o frases cortas que ayudarían al estudiante a corregirlo sin reescribirlo: \n\n{paragraph}"
        )
        feedback = prompt_gemini(msg)
        results.append({
            "paragraph_number": idx + 1,
            "type": tipo,
            "feedback": feedback
        })

    return results
