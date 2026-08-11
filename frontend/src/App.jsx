import React, { useCallback, useRef, useState } from "react";
import * as pdfjsLib from "pdfjs-dist";
import pdfjsWorker from "pdfjs-dist/build/pdf.worker.mjs?url";
import "./App.css";

pdfjsLib.GlobalWorkerOptions.workerSrc = pdfjsWorker;

// Relative path: the built frontend is served by the same Flask app,
// so this resolves against whatever host/port Flask is running on.
const API_URL = "/format-paper";

const STAGES = [
  { key: "submit", label: "Submit" },
  { key: "extract", label: "Extract" },
  { key: "typeset", label: "Typeset" },
  { key: "proof", label: "Proof" }
];

async function extractPdfText(file) {
  const buffer = await file.arrayBuffer();
  const pdf = await pdfjsLib.getDocument({ data: buffer }).promise;
  let fullText = "";

  for (let pageNum = 1; pageNum <= pdf.numPages; pageNum++) {
    const page = await pdf.getPage(pageNum);
    const content = await page.getTextContent();
    const pageText = content.items.map((item) => item.str).join(" ");
    fullText += `\n\n--- Page ${pageNum} ---\n${pageText}`;
  }

  return { text: fullText, pageCount: pdf.numPages };
}

function Stage({ index, label, active, done }) {
  return (
    <div className={`stage ${active ? "stage-active" : ""} ${done ? "stage-done" : ""}`}>
      <span className="stage-mark">{done ? "✓" : String(index + 1).padStart(2, "0")}</span>
      <span className="stage-label">{label}</span>
    </div>
  );
}

export default function App() {
  const [fileName, setFileName] = useState(null);
  const [extracting, setExtracting] = useState(false);
  const [pdfText, setPdfText] = useState("");
  const [pageCount, setPageCount] = useState(0);
  const [converting, setConverting] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);
  const [dragOver, setDragOver] = useState(false);
  const inputRef = useRef(null);

  const stageKey = converting
    ? "proof"
    : result
    ? "proof"
    : pdfText
    ? "typeset"
    : extracting
    ? "extract"
    : "submit";
  const stageIndex = STAGES.findIndex((s) => s.key === stageKey);

  const handleFile = useCallback(async (file) => {
    if (!file || file.type !== "application/pdf") {
      setError("Please submit a manuscript in PDF form.");
      return;
    }
    setError(null);
    setResult(null);
    setFileName(file.name);
    setExtracting(true);
    try {
      const { text, pageCount } = await extractPdfText(file);
      if (!text.trim()) {
        throw new Error(
          "This PDF contains no selectable text. Scanned/image-only PDFs are not supported."
        );
      }

      setPdfText(text);
      setPageCount(pageCount);
    } catch (err) {
      setError(`Could not read this PDF: ${err.message}`);
    } finally {
      setExtracting(false);
    }
  }, []);

  const onDrop = useCallback(
    (e) => {
      e.preventDefault();
      setDragOver(false);
      handleFile(e.dataTransfer.files?.[0]);
    },
    [handleFile]
  );

  const onConvert = async () => {
    setConverting(true);
    setError(null);
    setResult(null);
    try {
      const res = await fetch(API_URL, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ paper_content: pdfText })
      });

      const contentType = res.headers.get("content-type") || "";
      const data = contentType.includes("application/json")
        ? await res.json()
        : null;

      if (!res.ok) {
        throw new Error(
          data?.message || `Formatting pipeline failed (${res.status}).`
        );
      }

      if (!data?.pdf_url || !data?.latex_url || !data?.manuscript_url) {
        throw new Error("The server returned an incomplete formatting result.");
      }

      setResult(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setConverting(false);
    }
  };

  const reset = () => {
    setFileName(null);
    setPdfText("");
    setPageCount(0);
    setResult(null);
    setError(null);
    if (inputRef.current) inputRef.current.value = "";
  };

  return (
    <div className="page">
      <header className="masthead">
        <div className="masthead-inner">
          <p className="eyebrow">Manuscript Formatting Desk</p>
          <h1>ScholarFlow AI</h1>
          <p className="dek">
            Submit a draft, and the desk will extract, typeset, and proof it into a
            camera-ready paper.
          </p>
        </div>
      </header>

      <nav className="stages" aria-label="Pipeline progress">
        {STAGES.map((s, i) => (
          <Stage
            key={s.key}
            index={i}
            label={s.label}
            active={i === stageIndex}
            done={i < stageIndex}
          />
        ))}
      </nav>

      <main className="desk">
        {!fileName && (
          <div
            className={`dropzone ${dragOver ? "dropzone-active" : ""}`}
            onDragOver={(e) => {
              e.preventDefault();
              setDragOver(true);
            }}
            onDragLeave={() => setDragOver(false)}
            onDrop={onDrop}
            onClick={() => inputRef.current?.click()}
            role="button"
            tabIndex={0}
          >
            <span className="dropzone-mark">✎</span>
            <p className="dropzone-title">Drop a manuscript here</p>
            <p className="dropzone-sub">or click to browse — PDF only</p>
            <input
              ref={inputRef}
              type="file"
              accept="application/pdf"
              hidden
              onChange={(e) => handleFile(e.target.files?.[0])}
            />
          </div>
        )}

        {error && <p className="error-banner">{error}</p>}

        {extracting && <p className="status-line">Reading “{fileName}” …</p>}

        {fileName && !extracting && pdfText && (
          <section className="manuscript-card">
            <div className="manuscript-head">
              <div>
                <p className="manuscript-file">{fileName}</p>
                <p className="manuscript-sub">Extracted and ready for typesetting</p>
              </div>
              <button className="link-btn" onClick={reset}>
                Start over
              </button>
            </div>

            <div className="margin-notes">
              <span className="note note-pen">{pageCount} pages</span>
              <span className="note note-pen">{pdfText.length.toLocaleString()} characters</span>
            </div>

            <pre className="manuscript-preview">{pdfText.slice(0, 4000)}</pre>

            {!result && (
              <button className="primary-btn" onClick={onConvert} disabled={converting}>
                {converting ? "Typesetting…" : "Convert to LaTeX"}
              </button>
            )}
          </section>
        )}

        {result && (
          <section className="result-card">
            <p className="result-eyebrow">Proofed &amp; ready</p>
            <h2>Your paper has been typeset</h2>
            <div className="result-links">
              {result.pdf_url && (
                <a className="primary-btn" href={result.pdf_url} target="_blank" rel="noreferrer">
                  Download PDF
                </a>
              )}
              {result.latex_url && (
                <a className="ghost-btn" href={result.latex_url} target="_blank" rel="noreferrer">
                  Download .tex
                </a>
              )}
              {result.manuscript_url && (
                <a className="ghost-btn" href={result.manuscript_url} target="_blank" rel="noreferrer">
                  Download manuscript.md
                </a>
              )}
            </div>
          </section>
        )}
      </main>

      <footer className="foot-rule">
        <span>ScholarFlow AI · connects to the formatting service at localhost:5002</span>
      </footer>
    </div>
  );
}
