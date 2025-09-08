import { useState } from "react";
export default function Home() {
  const [prompt, setPrompt] = useState("trim 0:00-0:06; speed 1.25x");
  const [videoPath, setVideoPath] = useState("../examples/input.mp4");
  const [result, setResult] = useState(null);

  async function runPlan() {
    const res = await fetch("http://localhost:8000/plan", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ prompt }),
    });
    const js = await res.json();
    setResult(js);
  }

  async function runExecute() {
    const res = await fetch("http://localhost:8000/execute", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ prompt, video_path: videoPath }),
    });
    const js = await res.json();
    setResult(js);
  }

  return (
    <main style={{ maxWidth: 720, margin: "2rem auto", padding: 24 }}>
      <h1>Lens Prompt Editor (MVP)</h1>
      <p>Type a prompt and plan or execute. Backend must run on port 8000.</p>
      <textarea rows={4} style={{ width: "100%" }} value={prompt} onChange={e=>setPrompt(e.target.value)} />
      <div style={{ height: 12 }} />
      <input style={{ width: "100%" }} value={videoPath} onChange={e=>setVideoPath(e.target.value)} />
      <div style={{ height: 12 }} />
      <button onClick={runPlan}>Plan</button>{" "}
      <button onClick={runExecute}>Execute</button>
      <pre style={{ marginTop: 16, background: "#111", color: "#0f0", padding: 12, whiteSpace: "pre-wrap" }}>
        {result ? JSON.stringify(result, null, 2) : "No output yet"}
      </pre>
    </main>
  );
}
