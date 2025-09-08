from parser import parse_prompt

def test_parse_basic():
    ops = parse_prompt("trim 0:00-0:05; speed 1.25x; captions examples/sample.srt")
    kinds = [o["kind"] for o in ops]
    assert kinds == ["trim", "speed", "captions"]
