# Persian Wiki Semantic Search

A simple semantic search service for Persian Wikipedia titles using FastAPI, Qdrant, and Sentence Transformers.

## Features

- Semantic search over Persian Wikipedia titles
- FastAPI REST API
- Qdrant vector database
- Multilingual sentence embeddings
- Batch ingestion from `MaralGPT/persian-wikipedia`
- Persistent Qdrant storage with Docker

## Tech Stack

- Python
- FastAPI
- Qdrant
- Sentence Transformers
- Hugging Face Datasets
- Docker

## Model

This project uses:

```python
paraphrase-multilingual-MiniLM-L12-v2
```

It is more suitable for Persian than `all-MiniLM-L6-v2`.

## Dataset

Source dataset:

- `MaralGPT/persian-wikipedia`

Used fields:

- `id`
- `url`
- `title`
- `text`

Current ingestion focuses on `title`.

## Project Structure

```bash
project/
  app/
    __init__.py
    config.py
    models.py
    embedding_service.py
    qdrant_service.py
    dataset_ingestor.py
    api.py
  main.py
  ingest.py
```

## Setup

### 1) Clone the project

```bash
git clone https://github.com/aminmotamedi1400/persian-wiki-semantic-search.git
cd persian-wiki-semantic-search
```

### 2) Create virtual environment

```bash
python -m venv .venv
source .venv/bin/activate
```

On Windows:

```bash
.venv\Scripts\activate
```

### 3) Install dependencies

```bash
pip install fastapi uvicorn qdrant-client sentence-transformers datasets pydantic-settings
```

## Hugging Face Token

For better download speed and higher rate limits, set your Hugging Face token.

### Linux / macOS

```bash
export HF_TOKEN="your_token_here"
```

### Windows PowerShell

```powershell
$env:HF_TOKEN="your_token_here"
```

## Run Qdrant

Use persistent storage:

```bash
mkdir -p qdrant_data

docker run -d \
  --name qdrant_db \
  -p 6333:6333 \
  -v "$(pwd)/qdrant_data:/qdrant/storage" \
  qdrant/qdrant
```

## Run API

```bash
uvicorn main:app --reload
```

API will be available at:

- `http://127.0.0.1:8000`
- Swagger docs: `http://127.0.0.1:8000/docs`

## Ingest Dataset

To load a subset of Persian Wikipedia titles into Qdrant:

```bash
python ingest.py
```

You can control ingestion settings from `app/config.py`:

- `batch_size`
- `max_rows`
- `collection_name`
- `model_name`

## API Endpoints

### Health Check

```http
GET /
```

### Add Title

```http
POST /add-title
```

Request body:

```json
{
  "id": 1,
  "title": "صفحه اصلی",
  "wiki_id": "2",
  "url": "https://fa.wikipedia.org/wiki/صفحهٔ_اصلی"
}
```

### Search

```http
POST /search
```

Request body:

```json
{
  "text": "صفحه اصلی ویکی پدیا",
  "limit": 5
}
```

## Example cURL

### Add title

```bash
curl -X POST "http://127.0.0.1:8000/add-title" \
-H "Content-Type: application/json" \
-d '{
  "id": 1,
  "title": "صفحه اصلی",
  "wiki_id": "2",
  "url": "https://fa.wikipedia.org/wiki/صفحهٔ_اصلی"
}'
```

### Search

```bash
curl -X POST "http://127.0.0.1:8000/search" \
-H "Content-Type: application/json" \
-d '{
  "text": "صفحه اصلی ویکی پدیا",
  "limit": 5
}'
```

## Persistence

Qdrant data is stored in:

```bash
./qdrant_data
```

So your vectors remain available after container restart.

To stop and start the container:

```bash
docker stop qdrant_db
docker start qdrant_db
```

## Notes

- If you change the embedding model, vector size may change.
- In that case, recreate the Qdrant collection.
- Current implementation focuses on title embeddings only.

## Future Improvements

- Full article text ingestion
- Resume/checkpoint ingestion
- Metadata filters
- Better ranking pipeline
- Hybrid search
- Docker Compose setup
- Production-ready settings

## License

MIT
