from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from rapidfuzz import process, fuzz
import uvicorn

app = FastAPI(title="Fuzzy Search Service with AI Help")

# Map allowed scorers to RapidFuzz functions
SCORERS = {
    "WRatio": fuzz.WRatio,
    "ratio": fuzz.ratio,
    "partial_ratio": fuzz.partial_ratio,
    "token_sort_ratio": fuzz.token_sort_ratio,
    "token_set_ratio": fuzz.token_set_ratio
}

SCORER_DESCRIPTIONS = {
    "WRatio": "Best all-around scorer balancing multiple factors (default).",
    "ratio": "Simple Levenshtein distance (character edit distance).",
    "partial_ratio": "Matches if searched string is a substring of candidates.",
    "token_sort_ratio": "Ignores word order; good for shuffled words.",
    "token_set_ratio": "Handles duplicates well; good for noisy data."
}

class SearchRequest(BaseModel):
    searched_string: str
    searched_values: List[str]
    scorer: Optional[str] = "WRatio"  # Default scorer

class SearchResult(BaseModel):
    value: str
    score: int  # Truncated score

class SearchResponse(BaseModel):
    results: List[SearchResult]

@app.post("/fuzzy_search", response_model=SearchResponse)
async def fuzzy_search(request: SearchRequest):
    if not request.searched_values:
        raise HTTPException(status_code=400, detail="searched_values cannot be empty")
    
    scorer_func = SCORERS.get(request.scorer)
    if not scorer_func:
        raise HTTPException(status_code=400, detail=f"Invalid scorer. Available options: {list(SCORERS.keys())}")

    matches = process.extract(
        request.searched_string,
        request.searched_values,
        scorer=scorer_func,
        limit=10
    )

    response = SearchResponse(
        results=[SearchResult(value=match[0], score=int(match[1])) for match in matches]
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
            "searched_values": "List of strings you want to compare against.",
            "scorer": "(Optional) Scoring function to use. Available options with description below. Default is WRatio."
        },
        "scorers": SCORER_DESCRIPTIONS,
        "output_format": {
            "results": [{"value": "Matched string", "score": "Similarity score (0-100) as integer"}]
        },
        "example_input": {
            "searched_string": "apple",
            "searched_values": ["apple pie", "appl", "pineapple", "banana"],
            "scorer": "token_sort_ratio"
        },
        "example_output": {
            "results": [
                {"value": "apple pie", "score": 95},
                {"value": "appl", "score": 90}
            ]
        },
        "note": "The main application file is named 'fuzzy_search_service.py'"
    }

if __name__ == "__main__":
    uvicorn.run("fuzzy_search_service:app", host="0.0.0.0", port=8000)