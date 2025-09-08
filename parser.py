import re

TIME = r"(?:\d{1,2}:\d{2}(?::\d{2})?)"

def _parse_time(t: str) -> float:
    parts = [int(x) for x in t.split(":")]
    if len(parts) == 2:
        m, s = parts
        return m*60 + s
    if len(parts) == 3:
        h, m, s = parts
        return h*3600 + m*60 + s
    raise ValueError("Bad time format")

def parse_prompt(prompt: str):
    """
    Very small rule-based parser:
      - trim START-END
      - speed FACTORx
      - zoom FACTORx
      - captions PATH.srt
    Commands separated by ';' or ','
    """
    ops = []
    chunks = [c.strip() for c in re.split(r"[;,]", prompt) if c.strip()]

    for c in chunks:
        c_low = c.lower()

        m = re.search(rf"trim\s+({TIME})\s*-\s*({TIME})", c_low)
        if m:
            start = _parse_time(m.group(1))
            end = _parse_time(m.group(2))
            if end <= start:
                raise ValueError("trim end must be > start")
            ops.append({"kind":"trim","args":{"start": start, "end": end}})
            continue

        m = re.search(r"speed\s+([0-9]*\.?[0-9]+)x", c_low)
        if m:
            factor = float(m.group(1))
            ops.append({"kind":"speed","args":{"factor": factor}})
            continue

        m = re.search(r"zoom\s+([0-9]*\.?[0-9]+)x", c_low)
        if m:
            factor = float(m.group(1))
            ops.append({"kind":"zoom","args":{"factor": factor}})
            continue

        m = re.search(r"captions\s+(.+\.srt)", c_low)
        if m:
            path = m.group(1).strip()
            ops.append({"kind":"captions","args":{"path": path}})
            continue

        ops.append({"kind":"note","args":{"text": c}})

    return ops
