import json
from schemas import DDRReport
from dotenv import load_dotenv
from groq import Groq
import os
from prompt import DDR_SYSTEM_PROMPT, DDR_PROMPT

load_dotenv() 
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

import re

def clean_json(text):
    text = text.strip()
    text = text.replace("```json", "").replace("```", "")
    match = re.search(r"\{.*\}", text, re.DOTALL)
    return match.group(0) if match else text

def extract_observations(text, image_captions):

    prompt = DDR_PROMPT.format(
        TEXT=text,
        IMAGES=image_captions
    )

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": DDR_SYSTEM_PROMPT},
            {"role": "user", "content": prompt}],
            max_tokens=1500
    )
    # print("RAW all response:\n", response) 

    result = response.choices[0].message.content

    print("RAW LLM OUTPUT:\n", result) 

    cleaned_data = clean_json(result)

    data = json.loads(cleaned_data)

    return DDRReport(**data)
