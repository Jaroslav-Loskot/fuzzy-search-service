from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from rapidfuzz import process, fuzz
import uvicorn

app = FastAPI(title="Fuzzy Search Service with AI Help")

class SearchRequest(BaseModel):
    searched_string: str
    searched_values: List[str]

class SearchResult(BaseModel):
    value: str
    score: float

class SearchResponse(BaseModel):
    results: List[SearchResult]

@app.post("/fuzzy_search", response_model=SearchResponse)
async def fuzzy_search(request: SearchRequest):
    if not request.searched_values:
        raise HTTPException(status_code=400, detail="searched_values cannot be empty")

    matches = process.extract(
        request.searched_string,
        request.searched_values,
        scorer=fuzz.WRatio,
        limit=10
    )

    response = SearchResponse(
        results=[SearchResult(value=match[0], score=match[1]) for match in matches]
    )
    return response

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.get("/help")
async def help_service():
    return {
        "service": "Fuzzy Search Service",
        "description": "This service accepts a JSON with a search string and a list of candidate strings. It returns the top 10 most similar values using fuzzy matching.",
        "input_format": {
            "searched_string": "The string you are searching for.",
            "searched_values": "List of strings you want to compare against."
        },
        "output_format": {
            "results": [{"value": "Matched string", "score": "Similarity score (0-100)"}]
        },
        "example_input": {
            "searched_string": "apple",
            "searched_values": ["apple pie", "appl", "pineapple", "banana"]
        },
        "example_output": {
            "results": [
                {"value": "apple pie", "score": 95.0},
                {"value": "appl", "score": 90.0}
            ]
        },
        "note": "The main application file is named 'fuzzy_search_service.py'"
    }

if __name__ == "__main__":
    uvicorn.run("fuzzy_search_service:app", host="0.0.0.0", port=8000)
