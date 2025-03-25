import os
import json
from fastapi import FastAPI, HTTPException, Body
from langchain_community.document_loaders import PyPDFLoader
from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate
import re

app = FastAPI()

# Load API key from environment variable
groq_api_key = os.getenv("GROQ_API_KEY")
if not groq_api_key:
    raise ValueError("GROQ_API_KEY environment variable is not set")

# Initialize Groq client
chat_model = ChatGroq(temperature=0, groq_api_key=groq_api_key, model_name="llama3-70b-8192")

# PDF file mapping
PDF_FILES = {
    "H1": "LawsH1_167_179.pdf",
    "H2": "LawsH2_222_229.pdf"
}

def load_pdf_text(pdf_name):
    """ Load the PDF and return its text content. """
    try:
        pdf_path = os.path.join(os.path.dirname(__file__), pdf_name)
        loader = PyPDFLoader(pdf_path)
        pages = loader.load()
        return "\n".join([page.page_content for page in pages])
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"PDF loading failed: {str(e)}")

def extract_profiling_rules(pdf_text):
    """ Step 1: Extract profiling rules from the document. """
    try:
        prompt = PromptTemplate.from_template("""\
You are a compliance expert. Extract strict data profiling rules from the following document:

{pdf_text}

RULES GENERATED:
- List all inferred data profiling rules related to fields, formats, special character restrictions, number ranges, and any specific conditions.
- Be precise and include clear rule definitions.
""")
        
        formatted_prompt = prompt.format(pdf_text=pdf_text)
        response = chat_model.invoke(formatted_prompt)

        print(response.content.strip())

        return response.content.strip()  # Directly return extracted rules
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Rule extraction failed: {str(e)}")

@app.post("/check_compliance/{section}/")
async def validate_transaction(section: str, data: dict = Body(...)):
    """ Step 2: Use extracted rules to check transaction compliance based on section (H1 or H2). """
    try:
        # Validate section and select the correct PDF
        pdf_name = PDF_FILES.get(section.upper())
        if not pdf_name:
            raise HTTPException(status_code=400, detail="Invalid section. Use 'H1' or 'H2'.")

        # Load PDF and extract rules
        pdf_text = load_pdf_text(pdf_name)
        profiling_rules = extract_profiling_rules(pdf_text)

        # Compliance validation prompt
        prompt = PromptTemplate.from_template("""\
You are a compliance analysis system. Evaluate the transaction against the following profiling rules.:

{profiling_rules}

TRANSACTION:
{transaction}

*Instructions:*
- Check each key-value pair for compliance.
- Strictly follow profiling rules.
- Concentrate highest on Allowable values section.
- Determine if the value is *compliant or non-compliant* based on the rules.
- Calculate *risk_score*: (Non-compliant fields / Total fields) * 100
- Determine *violated_rules* as which rule has been violated for non-compliant fields
- Suggest *remedies* for non-compliant fields.
- Verify digits, special characters, and formats as per the rules.

**Response Format (Valid JSON only, no extra text):**
{{
  "compliant": "Yes" or "No",
  "risk_score": 1-100,
  "violated_rules": *violated_rules* with complete description for each rule,
  "remedies": *remedies* with complete description for each remedy
}}
""")

        formatted_prompt = prompt.format(
            profiling_rules=profiling_rules,
            transaction=json.dumps(data, indent=2)
        )

        response = chat_model.invoke(formatted_prompt)
        raw_response = response.content.strip()

        print(f"Model Response:\n{raw_response}\n")  # Debugging step

         # Extract JSON from response
        match = re.search(r'\{.*\}', raw_response, re.DOTALL)
        if match:
            json_response = match.group(0)
            return json.loads(json_response)
        else:
            raise ValueError("Model response does not contain valid JSON.")

    except json.JSONDecodeError:
        raise HTTPException(
            status_code=500,
            detail="Compliance check failed: Model response is not valid JSON."
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Compliance check failed: {str(e)}"
        )
