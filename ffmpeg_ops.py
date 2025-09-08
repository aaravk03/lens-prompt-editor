import os, subprocess, shlex, uuid

class FFmpegRunner:
    def __init__(self):
        pass

    def _run(self, cmd: str):
        print("Running:", cmd)
        proc = subprocess.run(shlex.split(cmd), capture_output=True, text=True)
        if proc.returncode != 0:
            raise RuntimeError(proc.stderr)
        return proc

    def run_pipeline(self, input_path: str, ops):
        current = input_path
        temp_files = []
        try:
            for op in ops:
                kind = op.get("kind")
                args = op.get("args", {})
                if kind == "note":
                    continue
                out = self._temp_name(current)

                if kind == "trim":
                    start = args["start"]; end = args["end"]; dur = end - start
                    cmd = f'ffmpeg -y -ss {start} -i "{current}" -t {dur} -c copy "{out}"'
                    self._run(cmd)

                elif kind == "speed":
                    factor = float(args["factor"])
                    setpts = 1.0 / factor
                    # audio atempo valid range 0.5-2.0; clamp for demo
                    atempo = factor
                    if atempo < 0.5: atempo = 0.5
                    if atempo > 2.0: atempo = 2.0
                    cmd = f'ffmpeg -y -i "{current}" -filter_complex "[0:v]setpts={setpts}*PTS[v];[0:a]atempo={atempo}[a]" -map "[v]" -map "[a]" "{out}"'
                    self._run(cmd)

                elif kind == "zoom":
                    factor = float(args["factor"])
                    # naive zoom by scale then crop back to original size
                    cmd = f'ffmpeg -y -i "{current}" -vf "scale=iw*{factor}:ih*{factor},crop=iw/{factor}:ih/{factor}" "{out}"'
                    self._run(cmd)

                elif kind == "captions":
                    path = args["path"]
                    cmd = f'ffmpeg -y -i "{current}" -vf "subtitles={path}" "{out}"'
                    self._run(cmd)

                else:
                    cmd = f'ffmpeg -y -i "{current}" -c copy "{out}"'
                    self._run(cmd)

                if current != input_path:
                    temp_files.append(current)
                current = out

            return current
        finally:
            for t in temp_files:
                if os.path.exists(t):
                    try: os.remove(t)
                    except: pass

    def _temp_name(self, base: str) -> str:
        stem, ext = os.path.splitext(base)
        return f"{stem}.out.{uuid.uuid4().hex[:6]}{ext or '.mp4'}"
