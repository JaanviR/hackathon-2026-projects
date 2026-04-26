import React, { useEffect, useRef, useState } from "react";
import {
  Activity,
  AlertTriangle,
  BadgeCheck,
  Bot,
  ChevronDown,
  ChevronRight,
  CreditCard,
  FileText,
  HeartPulse,
  Loader2,
  MessageSquare,
  Pill,
  QrCode,
  Send,
  Stethoscope,
  User,
  FileText as FileTextIcon,
} from "lucide-react";
import { generateBrief, getDrugWarnings, getPatient, getQr } from "./api/careRelayApi";
import { compactCondition, display, shortMedName, titleCase } from "./utils/format";
import DeepDive from "./DeepDive";

/* ═══════════════════════════════════════════════════════════
   Patient registry + view config
   ═══════════════════════════════════════════════════════════ */

const PATIENTS = [
  { id: "emerald", name: "Emerald468 Botsford977", initials: "EB", source: "api" },
  { id: "mitchell", name: "James R. Mitchell", initials: "JM", source: "static" },
];

const VIEWS = [
  { id: "snapshot", label: "Snapshot", icon: Stethoscope },
  { id: "deepDive", label: "Deep Dive", icon: Activity },
  { id: "chat",     label: "Chat",      icon: MessageSquare },
  { id: "idCard",   label: "ID Card",   icon: CreditCard },
];

const metricOrder = ["hba1c", "blood_pressure", "ldl", "egfr", "weight", "glucose"];

/* ═══════════════════════════════════════════════════════════
   App root
   ═══════════════════════════════════════════════════════════ */

export default function App() {
  const [activePatient, setActivePatient] = useState("emerald");
  const [activeView, setActiveView] = useState("snapshot");
  const [patientData, setPatientData] = useState(null);
  const [error, setError] = useState("");

  useEffect(() => {
    getPatient()
      .then(setPatientData)
      .catch(() => setError("Backend is not reachable. Start Flask at http://127.0.0.1:5000."));
  }, []);

  if (error) {
    return (
      <main className="center-screen">
        <div className="error-card">
          <AlertTriangle size={28} />
          <h1>CareRelay backend needed</h1>
          <p>{error}</p>
        </div>
      </main>
    );
  }

  if (!patientData) {
    return (
      <main className="center-screen">
        <Loader2 className="spin" size={32} />
        <p>Loading patient snapshot...</p>
      </main>
    );
  }

  function handlePatientClick(pid) {
    if (activePatient === pid) return; // already selected
    setActivePatient(pid);
    setActiveView("snapshot");
  }

  return (
    <div className="app">
      {/* ── Sidebar ── */}
      <aside className="sidebar">
        <div className="brand">
          <div className="brand-mark">CR</div>
          <div>
            <strong>CareRelay</strong>
            <span>Clinician snapshot</span>
          </div>
        </div>

        <nav className="nav">
          <div className="nav-section-label">Patients</div>
          {PATIENTS.map((p) => {
            const isActive = activePatient === p.id;
            return (
              <div key={p.id} className="patient-group">
                <button
                  className={`nav-item patient-item ${isActive ? "active-patient" : ""}`}
                  onClick={() => handlePatientClick(p.id)}
                >
                  <div className="patient-avatar-sm">{p.initials}</div>
                  <span className="patient-name-sidebar">{p.name}</span>
                  {isActive ? <ChevronDown size={14} /> : <ChevronRight size={14} />}
                </button>

                {isActive && (
                  <div className="sub-nav">
                    {VIEWS.map((view) => {
                      const Icon = view.icon;
                      return (
                        <button
                          className={`nav-item sub-nav-item ${activeView === view.id ? "active" : ""}`}
                          key={view.id}
                          onClick={() => setActiveView(view.id)}
                        >
                          <Icon size={15} />
                          {view.label}
                        </button>
                      );
                    })}
                  </div>
                )}
              </div>
            );
          })}
        </nav>

        <div className="sidebar-note">
          <BadgeCheck size={16} />
          Synthetic Synthea data. Not for clinical use.
        </div>
      </aside>

      {/* ── Main content ── */}
      <main className="main">
        <DisclaimerBanner text={patientData.disclaimer} />

        {/* ── Emerald (API-driven) ── */}
        {activePatient === "emerald" && activeView === "snapshot" && <Snapshot data={patientData} />}
        {activePatient === "emerald" && activeView === "deepDive" && <DeepDive data={patientData} />}
        {activePatient === "emerald" && activeView === "idCard"   && <IDCard data={patientData} />}
        {activePatient === "emerald" && activeView === "chat"     && <ChatPlaceholder patientName="Emerald468 Botsford977" />}

        {/* ── Mitchell (static HTML) ── */}
        {activePatient === "mitchell" && (activeView === "snapshot" || activeView === "deepDive") && (
          <MitchellEHR />
        )}
        {activePatient === "mitchell" && activeView === "idCard" && (
          <MitchellIDPlaceholder />
        )}
        {activePatient === "mitchell" && activeView === "chat" && (
          <MitchellChat />
        )}
      </main>
    </div>
  );
}

/* ═══════════════════════════════════════════════════════════
   Mitchell — iframe embed of the reference EHR HTML
   ═══════════════════════════════════════════════════════════ */

function MitchellEHR() {
  return (
    <section className="page" style={{ padding: 0 }}>
      <iframe
        src="/mitchell_ehr.html"
        title="James R. Mitchell EHR"
        className="mitchell-iframe"
      />
    </section>
  );
}

function MitchellIDPlaceholder() {
  return (
    <section className="page">
      <div className="placeholder-view">
        <CreditCard size={48} strokeWidth={1} />
        <h2>ID Card — James R. Mitchell</h2>
        <p>Medical ID card for this patient is not yet generated.<br />
        This feature will be available once the patient record is fully integrated.</p>
      </div>
    </section>
  );
}

/* ═══════════════════════════════════════════════════════════
   Chat placeholder (for both patients)
   ═══════════════════════════════════════════════════════════ */

function ChatPlaceholder({ patientName }) {
  return (
    <section className="page">
      <div className="placeholder-view chat-placeholder">
        <MessageSquare size={48} strokeWidth={1} />
        <h2>Clinical Chat</h2>
        <p>RAG-powered clinical Q&A for <strong>{patientName}</strong></p>
        <div className="chat-preview">
          <div className="chat-input-mock">
            <input
              type="text"
              placeholder={`Ask a question about ${patientName.split(" ")[0]}'s history...`}
              disabled
            />
            <button disabled>Send</button>
          </div>
          <span className="coming-soon-badge">Coming Soon</span>
        </div>
      </div>
    </section>
  );
}

/* ═══════════════════════════════════════════════════════════
   Mitchell RAG Chat — real implementation
   ═══════════════════════════════════════════════════════════ */

const API_BASE = "http://127.0.0.1:5000";

function MitchellChat() {
  const [messages, setMessages] = useState([
    {
      role: "assistant",
      content: "Hello! I have access to James Mitchell's full EHR record (28 pages). Ask me anything about his medical history, medications, lab results, or procedures.",
      sources: [],
    },
  ]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [pdfPage, setPdfPage] = useState(null);
  const messagesEndRef = useRef(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  async function handleSend() {
    const q = input.trim();
    if (!q || loading) return;

    const userMsg = { role: "user", content: q, sources: [] };
    setMessages((prev) => [...prev, userMsg]);
    setInput("");
    setLoading(true);

    try {
      const resp = await fetch(`${API_BASE}/api/chat`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question: q }),
      });
      const data = await resp.json();
      if (data.error) {
        setMessages((prev) => [
          ...prev,
          { role: "assistant", content: `Error: ${data.error}`, sources: [] },
        ]);
      } else {
        setMessages((prev) => [
          ...prev,
          {
            role: "assistant",
            content: data.answer,
            sources: data.sources || [],
            sourceType: data.source_type,
          },
        ]);
      }
    } catch (err) {
      setMessages((prev) => [
        ...prev,
        { role: "assistant", content: "Unable to reach the backend. Is Flask running?", sources: [] },
      ]);
    } finally {
      setLoading(false);
    }
  }

  function handleKeyDown(e) {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  }

  return (
    <section className="page" style={{ padding: 0 }}>
      <div className="chat-layout">
        {/* ── Chat panel ── */}
        <div className="chat-panel">
          <div className="chat-header">
            <MessageSquare size={18} />
            <h2>Clinical Chat — James R. Mitchell</h2>
            <span className="chat-badge">RAG · EHR PDF</span>
          </div>

          <div className="chat-messages">
            {messages.map((msg, i) => (
              <div key={i} className={`chat-msg ${msg.role}`}>
                <div className="chat-msg-avatar">
                  {msg.role === "user" ? "Dr" : "AI"}
                </div>
                <div className="chat-msg-body">
                  <div className="chat-msg-text">{msg.content}</div>
                  {msg.sources && msg.sources.length > 0 && (
                    <div className="chat-sources">
                      <span className="chat-sources-label">Sources:</span>
                      {msg.sources.map((s, j) => (
                        <button
                          key={j}
                          className="chat-source-btn"
                          onClick={() => setPdfPage(s.page)}
                          title={s.snippet}
                        >
                          📄 Page {s.page}
                        </button>
                      ))}
                      {msg.sourceType === "extractive" && (
                        <span className="chat-source-fallback">Extractive (LLM unavailable)</span>
                      )}
                    </div>
                  )}
                </div>
              </div>
            ))}
            {loading && (
              <div className="chat-msg assistant">
                <div className="chat-msg-avatar">AI</div>
                <div className="chat-msg-body">
                  <div className="chat-msg-text chat-loading">
                    <Loader2 className="spin" size={16} />
                    Searching EHR records...
                  </div>
                </div>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>

          <div className="chat-input-bar">
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={handleKeyDown}
              placeholder="Ask about medications, labs, procedures, history..."
              disabled={loading}
            />
            <button onClick={handleSend} disabled={loading || !input.trim()}>
              <Send size={18} />
            </button>
          </div>
        </div>

        {/* ── PDF viewer panel ── */}
        <div className={`pdf-panel ${pdfPage ? "open" : ""}`}>
          {pdfPage ? (
            <>
              <div className="pdf-panel-header">
                <span>EHR Document — Page {pdfPage}</span>
                <button className="pdf-close-btn" onClick={() => setPdfPage(null)}>✕</button>
              </div>
              <iframe
                src={`${API_BASE}/api/pdf/mitchell#page=${pdfPage}`}
                title="Mitchell EHR PDF"
                className="pdf-iframe"
              />
            </>
          ) : (
            <div className="pdf-placeholder">
              <FileTextIcon size={40} strokeWidth={1} />
              <p>Click a source citation to view the EHR document</p>
            </div>
          )}
        </div>
      </div>
    </section>
  );
}

/* ═══════════════════════════════════════════════════════════
   Shared components (unchanged)
   ═══════════════════════════════════════════════════════════ */

function DisclaimerBanner({ text }) {
  return (
    <div className="disclaimer">
      <AlertTriangle size={16} />
      {text}
    </div>
  );
}

function Snapshot({ data }) {
  return (
    <section className="page">
      <PatientHeader data={data} />
      <MetricGrid metrics={data.snapshot.latestMetrics} />
      <div className="snapshot-grid">
        <ClinicalState data={data} />
        <AIBriefPanel />
      </div>
      <div className="three-col">
        <AllergyPanel allergies={data.snapshot.allergies} />
        <ConditionsPanel conditions={data.snapshot.activeConditions} />
        <MedicationPanel medications={data.snapshot.currentMedications} />
      </div>
      <DrugWarnings medications={data.snapshot.currentMedications} />
    </section>
  );
}

function PatientHeader({ data }) {
  const patient = data.patient;
  return (
    <header className="patient-hero">
      <div>
        <div className="eyebrow">QR-linked synthetic patient record</div>
        <h1>{patient.name}</h1>
        <p>
          {titleCase(patient.gender)} · {patient.age} · MRN {patient.mrn}
        </p>
      </div>
      <div className="header-facts">
        <Fact label="Blood type" value={patient.bloodType} />
        <Fact label="Code status" value={patient.codeStatus} />
        <Fact label="Address" value={patient.address} />
      </div>
    </header>
  );
}

function Fact({ label, value }) {
  return (
    <div className="fact">
      <span>{label}</span>
      <strong>{display(value)}</strong>
    </div>
  );
}

function MetricGrid({ metrics }) {
  return (
    <div className="metric-grid">
      {metricOrder.map((key) => {
        const metric = metrics[key];
        if (!metric) return null;
        return (
          <article className="metric-card" key={key}>
            <span>{metric.label}</span>
            <strong>{metric.displayValue}</strong>
            <small>{metric.date}</small>
          </article>
        );
      })}
    </div>
  );
}

function ClinicalState({ data }) {
  return (
    <section className="panel clinical-state">
      <div className="panel-title">
        <HeartPulse size={18} />
        <h2>Clinical State At A Glance</h2>
      </div>
      <div className="status-pill">Structured snapshot</div>
      <p>{data.snapshot.aiStatusLine}</p>
      <div className="mini-stats">
        <span>{data.conditions.length} conditions</span>
        <span>{data.medications.length} medications</span>
        <span>{data.encounters.length} recent encounters</span>
      </div>
    </section>
  );
}

function AIBriefPanel() {
  const [brief, setBrief] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function handleBrief() {
    setLoading(true);
    setError("");
    try {
      setBrief(await generateBrief());
    } catch {
      setError("Unable to generate brief. Check backend and Hugging Face token.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <section className="panel">
      <div className="panel-title">
        <Bot size={18} />
        <h2>First Visit Brief</h2>
      </div>
      <button className="primary-button" disabled={loading} onClick={handleBrief}>
        {loading ? <Loader2 className="spin" size={16} /> : <FileText size={16} />}
        {loading ? "Generating..." : "Generate First Visit Brief"}
      </button>
      {error && <p className="error-text">{error}</p>}
      {brief && (
        <div className="brief-box">
          <p>{brief.brief}</p>
          <small>
            Source: {brief.source} · Model: {brief.model || "fallback"}
          </small>
        </div>
      )}
    </section>
  );
}

function AllergyPanel({ allergies }) {
  return (
    <section className="panel">
      <div className="panel-title danger-title">
        <AlertTriangle size={18} />
        <h2>Allergies</h2>
      </div>
      <div className="chip-wrap">
        {allergies.length ? (
          allergies.map((allergy) => (
            <span className="chip danger" key={allergy.name}>
              {compactCondition(allergy.name)}
            </span>
          ))
        ) : (
          <p className="muted">No allergies documented.</p>
        )}
      </div>
    </section>
  );
}

function ConditionsPanel({ conditions }) {
  return (
    <section className="panel">
      <div className="panel-title">
        <Activity size={18} />
        <h2>Active Conditions</h2>
      </div>
      <div className="chip-wrap">
        {conditions.slice(0, 12).map((condition) => (
          <span className="chip" key={condition.name}>
            {compactCondition(condition.name)}
          </span>
        ))}
      </div>
    </section>
  );
}

function MedicationPanel({ medications }) {
  return (
    <section className="panel">
      <div className="panel-title">
        <Pill size={18} />
        <h2>Current Medications</h2>
      </div>
      <div className="list">
        {medications.slice(0, 8).map((med) => (
          <div className="list-row" key={med.name}>
            <strong>{shortMedName(med.name)}</strong>
            <span>{med.status} · {med.authoredOn || "date unknown"}</span>
          </div>
        ))}
      </div>
    </section>
  );
}

function DrugWarnings({ medications }) {
  const [warnings, setWarnings] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function checkWarnings() {
    setLoading(true);
    setError("");
    try {
      const medNames = medications.slice(0, 5).map((med) => med.name);
      setWarnings(await getDrugWarnings(medNames));
    } catch {
      setError("Unable to check OpenFDA labels.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <section className="panel wide-panel">
      <div className="panel-title danger-title">
        <AlertTriangle size={18} />
        <h2>OpenFDA Medication Warnings</h2>
      </div>
      <button className="secondary-button" disabled={loading} onClick={checkWarnings}>
        {loading ? <Loader2 className="spin" size={16} /> : <Pill size={16} />}
        {loading ? "Checking..." : "Check Current Medications"}
      </button>
      {error && <p className="error-text">{error}</p>}
      {warnings && (
        <div className="warning-grid">
          {warnings.warnings.map((warning) => (
            <article className="warning-card" key={warning.medication}>
              <strong>{warning.medication}</strong>
              <p>{warning.interaction || warning.warning}</p>
              <small>{warning.source}</small>
            </article>
          ))}
        </div>
      )}
    </section>
  );
}

function IDCard({ data }) {
  const [qr, setQr] = useState(null);

  useEffect(() => {
    getQr().then(setQr).catch(() => setQr(null));
  }, []);

  const meds = data.snapshot.currentMedications.slice(0, 4);
  const allergies = data.snapshot.allergies;
  return (
    <section className="page">
      <div className="section-heading">
        <div>
          <div className="eyebrow">Patient-carried access</div>
          <h1>Medical ID Card</h1>
        </div>
      </div>
      <div className="card-stage">
        <article className="medical-card">
          <div className="card-topline">CareRelay Medical ID</div>
          <h2>{data.patient.name}</h2>
          <p>{titleCase(data.patient.gender)} · {data.patient.age} · MRN {data.patient.mrn}</p>
          <div className="card-section">
            <strong>Critical allergies</strong>
            <span>{allergies.map((item) => compactCondition(item.name)).join(", ") || "None documented"}</span>
          </div>
          <div className="card-section">
            <strong>Key medications</strong>
            <span>{meds.map((item) => shortMedName(item.name)).join(", ")}</span>
          </div>
          <div className="card-footer">Emergency contact: Demo placeholder</div>
        </article>

        <article className="medical-card back">
          <div className="card-topline">Scan for clinician snapshot</div>
          <div className="qr-box">
            {qr ? <img src={qr.qr} alt="CareRelay QR code" /> : <QrCode size={96} />}
          </div>
          <p>{qr?.url || "http://localhost:5173/patient/default"}</p>
          <div className="card-footer">Synthetic demo only. Not for clinical use.</div>
        </article>
      </div>
    </section>
  );
}
