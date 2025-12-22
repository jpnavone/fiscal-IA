import os
from openai import OpenAI
from dotenv import load_dotenv
import json

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def analyze_text(text):
    """
    Analyze text to extract keywords and summary using OpenAI GPT-4o-mini.
    
    Args:
        text (str): The text to analyze.
        
    Returns:
        dict: A dictionary containing 'keywords' (list) and 'summary' (str).
    """
    system_prompt = """
    You are a legal assistant. Your task is to analyze the provided text (a transcription of a legal complaint/denuncia).
    1. Extract the most important keywords (entities, crimes, locations, names).
    2. Write a concise summary of the complaint.
    3. Categorize the complaint into ONE of the following categories: 
       ['Robo', 'Violencia de Género', 'Estafa', 'Narcotráfico', 'Homicidio', 'Amenazas', 'Accidente de Tránsito', 'Otros'].
    
    Return the output in JSON format with keys: "keywords" (list of strings), "summary" (string), and "category" (string).
    """
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": text}
            ],
            response_format={"type": "json_object"}
        )
        
        content = response.choices[0].message.content
        result = json.loads(content)
        return result
    except Exception as e:
        print(f"Error during analysis: {e}")
        return {"keywords": [], "summary": "Error during analysis.", "category": "Desconocido"}
