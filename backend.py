from fastapi import FastAPI
import openai
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

# Enable CORS for frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_methods=["*"],
    allow_headers=["*"],
)

# Set OpenAI API key (Replace with your actual API Key)
openai.api_key = "AIzaSyBbdAp7iAhRbeUK51PlGGAG2OLgXIi_UPQ"

class CodeInput(BaseModel):
    code: str

def process_code(action, code):
    """Uses AI to run, debug, or optimize Python code."""
    prompt = ""

    if action == "run":
        prompt = f"Execute the following Python script and provide the output:\n```{code}```"
    elif action == "debug":
        prompt = f"Find and fix any bugs in the following Python script:\n```{code}```\nExplain what was fixed."
    elif action == "optimize":
        prompt = f"Optimize the following Python script for better performance while maintaining functionality:\n```{code}```"

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "system", "content": "You are an expert Python assistant."},
                  {"role": "user", "content": prompt}]
    )
    return response["choices"][0]["message"]["content"]

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
