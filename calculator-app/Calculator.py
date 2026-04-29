from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
import math
import re
from pathlib import Path

app = FastAPI()

# Mount static files
static_path = Path(__file__).parent / "Static"
if static_path.exists():
    app.mount("/static", StaticFiles(directory=str(static_path)), name="static")


class Calculator:
    @staticmethod
    def evaluate(expression: str) -> float:
        """Safely evaluate a mathematical expression"""
        # Remove whitespace
        expression = expression.replace(" ", "")
        
        # Validate input - only allow numbers, operators, and functions
        if not re.match(r"^[0-9+\-*/(). % sqrt sin cos tan log^]+$", expression):
            raise ValueError("Invalid characters in expression")
        
        # Replace sqrt with math.sqrt
        expression = expression.replace("sqrt", "math.sqrt")
        expression = expression.replace("sin", "math.sin")
        expression = expression.replace("cos", "math.cos")
        expression = expression.replace("tan", "math.tan")
        expression = expression.replace("log", "math.log10")
        expression = expression.replace("^", "**")
        
        try:
            result = eval(expression, {"__builtins__": {}}, {"math": math})
            return float(result)
        except Exception as e:
            raise ValueError(f"Calculation error: {str(e)}")


@app.get("/")
async def root():
    """Serve the calculator index page"""
    return {"message": "Calculator API running. Visit /static for the UI"}


@app.post("/api/calc")
async def calculate(expression: str = None):
    """Calculate the result of a mathematical expression"""
    if not expression:
        return JSONResponse({"error": "No expression provided"}, status_code=400)
    
    try:
        result = Calculator.evaluate(expression)
        return JSONResponse({"expression": expression, "result": result, "error": None})
    except Exception as e:
        return JSONResponse({"expression": expression, "result": None, "error": str(e)}, status_code=400)


@app.get("/api/calc")
async def calculate_get(expression: str = None):
    """Calculate the result of a mathematical expression (GET method)"""
    if not expression:
        return JSONResponse({"error": "No expression provided"}, status_code=400)
    
    try:
        result = Calculator.evaluate(expression)
        return JSONResponse({"expression": expression, "result": result, "error": None})
    except Exception as e:
        return JSONResponse({"expression": expression, "result": None, "error": str(e)}, status_code=400)


if __name__ == "__main__":
    import uvicorn
    import os
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)