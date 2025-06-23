# Fuzzy Search Service

This project provides a REST API for fuzzy string matching using FastAPI and RapidFuzz.
It accepts a search string and a list of candidate values, and returns the top 10 most similar matches ranked by similarity score.

---

## Features

* 🔎 Multiple fuzzy search algorithms (`WRatio`, `ratio`, `partial_ratio`, `token_sort_ratio`, `token_set_ratio`)
* 🩺 Docker healthcheck endpoint
* 🤖 Self-documenting `/help` endpoint
* ⚡ Lightweight FastAPI backend with Docker support

---

## API Endpoints

### `POST /fuzzy_search`

Perform fuzzy search.

#### Request Body

```json
{
  "searched_string": "string",
  "searched_values": ["value1", "value2", "value3"],
  "scorer": "WRatio"  // Optional, default is WRatio
}
```

✅ Available scorers:

* `WRatio` (default)
* `ratio`
* `partial_ratio`
* `token_sort_ratio`
* `token_set_ratio`

#### Response

```json
{
  "results": [
    { "value": "matched string", "score": 95 },
    ...
  ]
}
```

---

### `GET /health`

Simple health check.

Response:

```json
{ "status": "ok" }
```

---

### `GET /help`

Returns full service description with input/output examples.

---

## Example Usage

### Example Request

```bash
curl -X POST http://localhost:8000/fuzzy_search \
-H "Content-Type: application/json" \
-d '{
  "searched_string": "apple",
  "searched_values": ["apple pie", "appl", "pineapple", "banana"],
  "scorer": "token_sort_ratio"
}'
```

### Example Response

```json
{
  "results": [
    { "value": "apple pie", "score": 95.2 },
    { "value": "appl", "score": 90.1 }
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
uvicorn fuzzy_search_service:app --reload
```

### 2️⃣ Docker

#### Build Docker image

```bash
docker build -t fuzzy-search-service .
```

#### Run container

```bash
docker run -p 8000:8000 fuzzy-search-service
```

#### Or via Docker Compose (if you have multiple services):

```bash
docker-compose up
```

---

## Docker Compose (Example)

```yaml
services:
  fuzzy-search-service:
    build: .
    ports:
      - "8002:8000"
    networks:
      - supabase_default

networks:
  supabase_default:
    external: true
```

*Inside Docker network, call it via:*

```
http://fuzzy-search-service:8000/fuzzy_search
```

---

## Project Structure

```bash
.
├── fuzzy_search_service.py  # Main application code
├── requirements.txt
├── Dockerfile
├── .dockerignore
├── .gitignore
├── README.md
└── docker-compose.yml
```

---

## License

MIT License

---