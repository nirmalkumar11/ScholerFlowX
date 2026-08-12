import React, { useCallback, useRef, useState } from "react";
import * as pdfjsLib from "pdfjs-dist";
import pdfjsWorker from "pdfjs-dist/build/pdf.worker.mjs?url";
import "./App.css";


// ============================================================================
// PDF.JS WORKER
// ============================================================================

pdfjsLib.GlobalWorkerOptions.workerSrc = pdfjsWorker;


// ============================================================================
// API CONFIGURATION
// ============================================================================
//
// Local development:
// VITE_API_URL=http://localhost:5002
//
// Production:
// VITE_API_URL=https://scholerflowxx.onrender.com
//
// The endpoint (/format-paper) is added below.
// ============================================================================

const API_URL = (
  import.meta.env.VITE_API_URL || "http://localhost:5002"
).replace(/\/+$/, "");

console.log("API_URL =", API_URL);
console.log("API_URL =", API_URL);
console.log("FORMAT_ENDPOINT =", FORMAT_ENDPOINT);


// ============================================================================
// API ENDPOINTS
// ============================================================================

const FORMAT_ENDPOINT = `${API_URL}/format-paper`;

const PDF_ENDPOINT = `${API_URL}/download/pdf`;

const LATEX_ENDPOINT = `${API_URL}/download/tex`;

const MANUSCRIPT_ENDPOINT = `${API_URL}/download/manuscript`;


// ============================================================================
// PIPELINE STAGES
// ============================================================================

const STAGES = [
  { key: "submit", label: "Submit" },
  { key: "extract", label: "Extract" },
  { key: "typeset", label: "Typeset" },
  { key: "proof", label: "Proof" },
];


// ============================================================================
// PDF TEXT EXTRACTION
// ============================================================================

async function extractPdfText(file) {
  const buffer = await file.arrayBuffer();

  const pdf = await pdfjsLib.getDocument({
    data: buffer,
  }).promise;

  let fullText = "";

  for (
    let pageNum = 1;
    pageNum <= pdf.numPages;
    pageNum++
  ) {
    const page = await pdf.getPage(pageNum);

    const content = await page.getTextContent();

    const pageText = content.items
      .map((item) => item.str)
      .join(" ");

    fullText += `\n\n--- Page ${pageNum} ---\n${pageText}`;
  }

  return {
    text: fullText,
    pageCount: pdf.numPages,
  };
}


// ============================================================================
// STAGE COMPONENT
// ============================================================================

function Stage({
  index,
  label,
  active,
  done,
}) {
  return (
    <div
      className={`stage ${
        active ? "stage-active" : ""
      } ${
        done ? "stage-done" : ""
      }`}
    >
      <span className="stage-mark">
        {done
          ? "✓"
          : String(index + 1).padStart(2, "0")}
      </span>

      <span className="stage-label">
        {label}
      </span>
    </div>
  );
}


// ============================================================================
// MAIN APPLICATION
// ============================================================================

export default function App() {

  const [fileName, setFileName] = useState(null);

  const [extracting, setExtracting] =
    useState(false);

  const [pdfText, setPdfText] =
    useState("");

  const [pageCount, setPageCount] =
    useState(0);

  const [converting, setConverting] =
    useState(false);

  const [result, setResult] =
    useState(null);

  const [error, setError] =
    useState(null);

  const [dragOver, setDragOver] =
    useState(false);

  const inputRef =
    useRef(null);


  // ==========================================================================
  // CURRENT PIPELINE STAGE
  // ==========================================================================

  const stageKey = converting
    ? "proof"
    : result
    ? "proof"
    : pdfText
    ? "typeset"
    : extracting
    ? "extract"
    : "submit";

  const stageIndex =
    STAGES.findIndex(
      (s) => s.key === stageKey
    );


  // ==========================================================================
  // HANDLE PDF
  // ==========================================================================

  const handleFile = useCallback(
    async (file) => {

      if (
        !file ||
        file.type !== "application/pdf"
      ) {
        setError(
          "Please submit a manuscript in PDF form."
        );

        return;
      }

      setError(null);
      setResult(null);
      setFileName(file.name);
      setExtracting(true);

      try {

        const {
          text,
          pageCount,
        } = await extractPdfText(file);

        if (!text.trim()) {
          throw new Error(
            "This PDF contains no selectable text. Scanned/image-only PDFs are not supported."
          );
        }

        setPdfText(text);
        setPageCount(pageCount);

      } catch (err) {

        setError(
          `Could not read this PDF: ${err.message}`
        );

      } finally {

        setExtracting(false);
      }
    },
    []
  );


  // ==========================================================================
  // DRAG AND DROP
  // ==========================================================================

  const onDrop = useCallback(
    (e) => {

      e.preventDefault();

      setDragOver(false);

      handleFile(
        e.dataTransfer.files?.[0]
      );
    },
    [handleFile]
  );


  // ==========================================================================
  // FORMAT PAPER
  // ==========================================================================

  const onConvert = async () => {

    if (!pdfText.trim()) {
      setError(
        "No extracted paper text is available."
      );

      return;
    }

    setConverting(true);
    setError(null);
    setResult(null);

    try {

      console.log(
        "Sending formatting request to:",
        FORMAT_ENDPOINT
      );

      // ----------------------------------------------------------------------
      // POST TO RENDER BACKEND
      // ----------------------------------------------------------------------

      const res = await fetch(
        FORMAT_ENDPOINT,
        {
          method: "POST",

          headers: {
            "Content-Type":
              "application/json",
          },

          body: JSON.stringify({
            paper_content: pdfText,
          }),
        }
      );


      // ----------------------------------------------------------------------
      // READ RESPONSE
      // ----------------------------------------------------------------------

      const contentType =
        res.headers.get(
          "content-type"
        ) || "";

      const data =
        contentType.includes(
          "application/json"
        )
          ? await res.json()
          : null;


      // ----------------------------------------------------------------------
      // HTTP ERROR
      // ----------------------------------------------------------------------

      if (!res.ok) {

        throw new Error(
          data?.message ||
            `Formatting pipeline failed (${res.status}).`
        );
      }


      // ----------------------------------------------------------------------
      // BACKEND ERROR
      // ----------------------------------------------------------------------

      if (
        data?.status === "error"
      ) {

        throw new Error(
          data.message ||
            "The formatting service returned an error."
        );
      }


      // ----------------------------------------------------------------------
      // VALIDATE RESPONSE
      // ----------------------------------------------------------------------

      if (
        !data?.pdf_url ||
        !data?.latex_url ||
        !data?.manuscript_url
      ) {

        throw new Error(
          "The server returned an incomplete formatting result."
        );
      }


      // ----------------------------------------------------------------------
      // SUCCESS
      // ----------------------------------------------------------------------

      console.log(
        "Formatting completed successfully:",
        data
      );

      setResult(data);

    } catch (err) {

      console.error(
        "Formatting request failed:",
        err
      );

      // Handle browser-level network errors.
      if (
        err instanceof TypeError &&
        err.message === "Failed to fetch"
      ) {
        setError(
          `Could not connect to the formatting service at ${API_URL}. Check the Vercel API URL and backend CORS configuration.`
        );
      } else {
        setError(
          err.message ||
            "Formatting failed."
        );
      }

    } finally {

      setConverting(false);
    }
  };


  // ==========================================================================
  // RESET
  // ==========================================================================

  const reset = () => {

    setFileName(null);

    setPdfText("");

    setPageCount(0);

    setResult(null);

    setError(null);

    setExtracting(false);

    setConverting(false);

    if (inputRef.current) {
      inputRef.current.value = "";
    }
  };


  // ==========================================================================
  // UI
  // ==========================================================================

  return (
    <div className="page">

      {/* ================================================================== */}
      {/* HEADER */}
      {/* ================================================================== */}

      <header className="masthead">

        <div className="masthead-inner">

          <p className="eyebrow">
            Manuscript Formatting Desk
          </p>

          <h1>
            ScholarFlow AI
          </h1>

          <p className="dek">
            Submit a draft, and the desk
            will extract, typeset, and proof
            it into a camera-ready paper.
          </p>

        </div>

      </header>


      {/* ================================================================== */}
      {/* PIPELINE STAGES */}
      {/* ================================================================== */}

      <nav
        className="stages"
        aria-label="Pipeline progress"
      >

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


      {/* ================================================================== */}
      {/* MAIN CONTENT */}
      {/* ================================================================== */}

      <main className="desk">

        {/* ================================================================ */}
        {/* UPLOAD */}
        {/* ================================================================ */}

        {!fileName && (

          <div
            className={`dropzone ${
              dragOver
                ? "dropzone-active"
                : ""
            }`}
            onDragOver={(e) => {

              e.preventDefault();

              setDragOver(true);
            }}
            onDragLeave={() =>
              setDragOver(false)
            }
            onDrop={onDrop}
            onClick={() =>
              inputRef.current?.click()
            }
            role="button"
            tabIndex={0}
          >

            <span className="dropzone-mark">
              ✎
            </span>

            <p className="dropzone-title">
              Drop a manuscript here
            </p>

            <p className="dropzone-sub">
              or click to browse — PDF only
            </p>

            <input
              ref={inputRef}
              type="file"
              accept="application/pdf"
              hidden
              onChange={(e) =>
                handleFile(
                  e.target.files?.[0]
                )
              }
            />

          </div>

        )}


        {/* ================================================================ */}
        {/* ERROR */}
        {/* ================================================================ */}

        {error && (
          <p className="error-banner">
            {error}
          </p>
        )}


        {/* ================================================================ */}
        {/* EXTRACTION */}
        {/* ================================================================ */}

        {extracting && (

          <p className="status-line">
            Reading “{fileName}” …
          </p>

        )}


        {/* ================================================================ */}
        {/* MANUSCRIPT PREVIEW */}
        {/* ================================================================ */}

        {fileName &&
          !extracting &&
          pdfText && (

            <section className="manuscript-card">

              <div className="manuscript-head">

                <div>

                  <p className="manuscript-file">
                    {fileName}
                  </p>

                  <p className="manuscript-sub">
                    Extracted and ready for
                    typesetting
                  </p>

                </div>

                <button
                  className="link-btn"
                  onClick={reset}
                >
                  Start over
                </button>

              </div>


              <div className="margin-notes">

                <span className="note note-pen">
                  {pageCount} pages
                </span>

                <span className="note note-pen">
                  {pdfText.length.toLocaleString()}{" "}
                  characters
                </span>

              </div>


              <pre className="manuscript-preview">
                {pdfText.slice(0, 4000)}
              </pre>


              {!result && (

                <button
                  className="primary-btn"
                  onClick={onConvert}
                  disabled={converting}
                >
                  {converting
                    ? "Typesetting…"
                    : "Convert to LaTeX"}
                </button>

              )}

            </section>

          )}


        {/* ================================================================ */}
        {/* RESULT */}
        {/* ================================================================ */}

        {result && (

          <section className="result-card">

            <p className="result-eyebrow">
              Proofed &amp; ready
            </p>

            <h2>
              Your paper has been typeset
            </h2>


            <div className="result-links">

              {result.pdf_url && (

                <a
                  className="primary-btn"
                  href={result.pdf_url}
                  target="_blank"
                  rel="noreferrer"
                >
                  Download PDF
                </a>

              )}


              {result.latex_url && (

                <a
                  className="ghost-btn"
                  href={result.latex_url}
                  target="_blank"
                  rel="noreferrer"
                >
                  Download .tex
                </a>

              )}


              {result.manuscript_url && (

                <a
                  className="ghost-btn"
                  href={result.manuscript_url}
                  target="_blank"
                  rel="noreferrer"
                >
                  Download manuscript.md
                </a>

              )}

            </div>

          </section>

        )}

      </main>


      {/* ================================================================== */}
      {/* FOOTER */}
      {/* ================================================================== */}

      <footer className="foot-rule">

        <span>
          ScholarFlow AI · connected to the
          research formatting service
        </span>

      </footer>

    </div>
  );
}