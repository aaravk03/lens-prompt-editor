from fastapi import FastAPI
from pydantic import BaseModel, Field
import os
from parser import parse_prompt
from ffmpeg_ops import FFmpegRunner

api = FastAPI(title="Lens Prompt Editor API", version="0.1.0")

class PlanRequest(BaseModel):
    prompt: str = Field(..., description="e.g. 'trim 0:00-0:06; zoom 1.2x; speed 1.25x; captions examples/sample.srt'")

class ExecuteRequest(BaseModel):
    video_path: str
    prompt: str

@api.post("/plan")
def plan(req: PlanRequest):
    ops = parse_prompt(req.prompt)
    return {"prompt": req.prompt, "plan": ops}

@api.post("/execute")
def execute(req: ExecuteRequest):
    ops = parse_prompt(req.prompt)
    if not os.path.exists(req.video_path):
        return {"ok": False, "error": f"Video not found: {req.video_path}"}
    runner = FFmpegRunner()
    out_path = runner.run_pipeline(req.video_path, ops)
    return {"ok": True, "output": out_path, "ops": ops}
