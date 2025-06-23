# Fuzzy Search Service

This project provides a simple REST API for fuzzy string matching using FastAPI and RapidFuzz.
It accepts a search string and a list of candidate values, and returns the top 10 most similar matches ranked by similarity score.

## Features

* 🚀 Fast fuzzy matching using `rapidfuzz`
* 🩺 Docker healthcheck endpoint
* 🤖 AI-style self-documentation via `/help` endpoint
* ⚡ Lightweight FastAPI backend

## API Endpoints

### `POST /fuzzy_search`

Perform fuzzy search.

#### Request Body

```json
{
  "searched_string": "string",
  "searched_values": ["value1", "value2", "value3"]
}
```

#### Response

```json
{
  "results": [
    { "value": "closest match", "score": 95.0 },
    ...
  ]
}
```

### `GET /health`

Returns service health status:

```json
{ "status": "ok" }
```

### `GET /help`

Returns service description, input format, and examples.

---

## Example Usage

### Request

```bash
curl -X POST http://localhost:8000/fuzzy_search \
-H "Content-Type: application/json" \
-d '{
  "searched_string": "apple",
  "searched_values": ["apple pie", "appl", "pineapple", "banana"]
}'
```

### Response

```json
{
  "results": [
    { "value": "apple pie", "score": 95.0 },
    { "value": "appl", "score": 90.0 },
    { "value": "pineapple", "score": 77.0 },
    { "value": "banana", "score": 27.0 }
  ]
}
```

---

## Installation

### 1️⃣ Local (Python)

```bash
git clone <repository_url>
cd <repository>
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn fuzzy-search-service:app --reload
```

### 2️⃣ Docker

#### Build image

```bash
docker build -t fuzzy-search-service .
```

#### Run container

```bash
docker run -p 8000:8000 fuzzy-search-service
```

Healthcheck available at:
`http://localhost:8000/health`

---

## Dependencies

* `fastapi`
* `uvicorn[standard]`
* `rapidfuzz`
* `pydantic`

Install them via:

```bash
pip install fastapi uvicorn[standard] rapidfuzz
```

---

## License

MIT License

---