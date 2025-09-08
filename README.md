# Lens Prompt Editor (MVP)
Natural-language prompts that compile into simple video edits (ffmpeg under the hood).

**Why**: Timelines are powerful but slow for common, declarative edits.  
**What**: A minimal slice that turns prompts into an operation plan and executes with ffmpeg.

## Quickstart (Backend)
```bash
cd backend
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app:api --reload
```
API: http://localhost:8000

### Try it
```bash
# Plan from a prompt
curl -X POST http://localhost:8000/plan   -H "Content-Type: application/json"   -d '{"prompt":"trim 0:00-0:06; speed 1.25x; captions examples/sample.srt"}'

# Execute on your video (place input.mp4 under /examples)
curl -X POST http://localhost:8000/execute   -H "Content-Type: application/json"   -d '{"video_path":"../examples/input.mp4","prompt":"trim 0:00-0:06; speed 1.25x"}'
```

## Optional Frontend (skeleton)
```bash
cd ../frontend
npm install
npm run dev
# open http://localhost:3000
```

## Status
MVP for evaluation/learning; not production-ready.

## Roadmap
- Web UI to call /execute
- Richer parser (LLM function-calling or grammar)
- Social presets (9:16, 1:1) and smart crops
- Preview thumbnails
