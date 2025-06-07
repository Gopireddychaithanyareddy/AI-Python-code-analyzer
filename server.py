from fastapi import FastAPI
import google.generativeai as genai
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
API_KEY = os.getenv("APIKEY")

# Configure Google Gemini AI
genai.configure(api_key=API_KEY)

# Initialize FastAPI app
app = FastAPI()

# Enable CORS for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow requests from all domains (change in production)
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request Model
class CodeInput(BaseModel):
    code: str

def process_code(action, code):
    """Uses Google Gemini AI to run, debug, or optimize Python code."""
    prompt = ""

    if action == "run":
        prompt = f"Execute the following Python script and provide the output:\n```{code}```"
    elif action == "debug":
        prompt = f"Find and fix any bugs in the following Python script:\n```{code}```\nExplain what was fixed."
    elif action == "optimize":
        prompt = f"Optimize the following Python script for better performance while maintaining functionality:\n```{code}```"

    try:
        model = genai.GenerativeModel("gemini-pro")
        response = model.generate_content(prompt)

        return response.text if response.text else "⚠️ No response from Gemini AI."
    except Exception as e:
        return f"❌ Error processing code: {str(e)}"

@app.post("/run/")
async def run_code(data: CodeInput):
    result = process_code("run", data.code)
    return {"result": result}

@app.post("/debug/")
async def debug_code(data: CodeInput):
    result = process_code("debug", data.code)
    return {"result": result}

@app.post("/optimize/")
async def optimize_code(data: CodeInput):
    result = process_code("optimize", data.code)
    return {"result": result}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
