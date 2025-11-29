"use client";
import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";

export default function PatientDashboard() {
  // ----------------------------
  // STATE HOOKS (must be at top)
  // ----------------------------
  const [view, setView] = useState("home");
  const [moodHistory, setMoodHistory] = useState([]);
  const [doctorAssessments, setDoctorAssessments] = useState([]);
  const [prescriptions, setPrescriptions] = useState([]);
  const [error, setError] = useState("");

  const router = useRouter();

  const apiUrl = process.env.NEXT_PUBLIC_API_URL;
  const token =
    typeof window !== "undefined" ? localStorage.getItem("token") : null;
  const userId =
    typeof window !== "undefined" ? localStorage.getItem("user_id") : null;

  // ----------------------------
  // Redirect if not patient
  // ----------------------------
  useEffect(() => {
    const role = localStorage.getItem("role");
    if (!token || role !== "patient") router.push("/login");
  }, []);

  // ----------------------------
  // Load data based on selected view
  // ----------------------------
  useEffect(() => {
    if (view === "doctor") loadDoctorAssessments();
    if (view === "prescriptions") loadPrescriptions();
    if (view === "mood") loadMoodHistory();
  }, [view]);

  // ----------------------------
  // Fetch Mood History
  // ----------------------------
  async function loadMoodHistory() {
    try {
      const res = await fetch(`${apiUrl}/mood_history/user/${userId}`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      if (!res.ok) throw new Error("Failed to load mood history");
      setMoodHistory(await res.json());
    } catch (err) {
      setError(err.message);
    }
  }

  // ----------------------------
  // Fetch Doctor Assessments
  // ----------------------------
  async function loadDoctorAssessments() {
    try {
      const res = await fetch(`${apiUrl}/consultations/user/${userId}`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      if (!res.ok) throw new Error("Failed to load doctor assessments");
      setDoctorAssessments(await res.json());
    } catch (err) {
      setError(err.message);
    }
  }

  // ----------------------------
  // Fetch Prescriptions
  // ----------------------------
  async function loadPrescriptions() {
    try {
      const res = await fetch(
        `${apiUrl}/consultations/prescriptions/user/${userId}`,
        {
          headers: { Authorization: `Bearer ${token}` },
        }
      );
      if (!res.ok) throw new Error("Failed to load prescriptions");
      setPrescriptions(await res.json());
    } catch (err) {
      setError(err.message);
    }
  }

  // ==========================================================
  // HOME VIEW
  // ==========================================================
  if (view === "home") {
    return (
      <div
        className="min-h-screen bg-cover bg-center p-10 flex flex-col items-center justify-center"
        style={{ backgroundImage: "url('/background.png')" }}
      >
        <div className="bg-white/70 backdrop-blur-md rounded-2xl shadow-2xl p-8 w-full max-w-3xl text-center border border-white/40">
          {/* Logout aligned right */}
          <div className="flex justify-end mb-4">
            <button
              onClick={() => {
                localStorage.clear();
                router.push("/login");
              }}
              className="bg-red-500/80 text-white px-5 py-2 rounded-lg shadow hover:bg-red-600 transition-all duration-200 hover:scale-105"
            >
              Logout
            </button>
          </div>

          <h2 className="text-2xl font-extrabold text-blue-800 mb-6 drop-shadow">
            Patient Dashboard
          </h2>

          {/* Interactive Buttons */}
          <div className="flex flex-col gap-4">
            <DashButton
              color="from-blue-500 to-blue-700"
              onClick={() => router.push("/dashboard/patient/assessment")}
              label="🧠 Take Assessment"
            />

            <DashButton
              color="from-indigo-500 to-indigo-700"
              onClick={() => setView("mood")}
              label="📈 Show Mood History"
            />

            <DashButton
              color="from-green-500 to-green-700"
              onClick={() => setView("doctor")}
              label="🩺 Show Doctor’s Assessments"
            />

            <DashButton
              color="from-purple-500 to-purple-700"
              onClick={() => setView("prescriptions")}
              label="💊 Show Prescriptions"
            />
          </div>
        </div>
      </div>
    );
  }

  // ==========================================================
  // MOOD HISTORY VIEW
  // ==========================================================
  if (view === "mood") {
    return (
      <DashboardSection title="Mood History" setView={setView}>
        {moodHistory.length === 0 ? (
          <p>No mood history available.</p>
        ) : (
          moodHistory.map((m, i) => (
            <div key={i} className="bg-white/80 p-4 rounded shadow mb-3">
              <span>{new Date(m.timestamp).toLocaleDateString()}</span>
              <span className="font-bold text-purple-600 ml-4">
                Score: {m.mood_score}
              </span>
            </div>
          ))
        )}
      </DashboardSection>
    );
  }

  // ==========================================================
  // DOCTOR ASSESSMENTS VIEW
  // ==========================================================
  if (view === "doctor") {
    return (
      <DashboardSection title="Doctor’s Assessments" setView={setView}>
        {doctorAssessments.length === 0 ? (
          <p>No assessments found.</p>
        ) : (
          doctorAssessments.map((a) => (
            <div key={a.id} className="bg-white/80 p-4 rounded shadow mb-3">
              <p>
                <strong>Date:</strong>{" "}
                {new Date(a.date).toLocaleDateString()}
              </p>
              <p>
                <strong>Doctor:</strong> {a.doctor_name}
              </p>
              <p>
                <strong>Notes:</strong> {a.notes || "No notes provided"}
              </p>
            </div>
          ))
        )}
      </DashboardSection>
    );
  }

  // ==========================================================
  // PRESCRIPTIONS VIEW
  // ==========================================================
  if (view === "prescriptions") {
    return (
      <DashboardSection title="Your Prescriptions" setView={setView}>
        {prescriptions.length === 0 ? (
          <p>No prescriptions found.</p>
        ) : (
          prescriptions.map((p) => (
            <div key={p.id} className="bg-white/80 p-4 rounded shadow mb-3">
              <p>
                <strong>Medication:</strong> {p.medicine_name}
              </p>
              <p>
                <strong>Dosage:</strong> {p.dosage}
              </p>
              <p>
                <strong>Instructions:</strong> {p.instructions}
              </p>
              {p.pharmacy && (
                <div className="mt-2 text-sm text-gray-700">
                  <p>
                    <strong>Pharmacy:</strong> {p.pharmacy.name}
                  </p>
                  <p>{p.pharmacy.address}</p>
                </div>
              )}
            </div>
          ))
        )}
      </DashboardSection>
    );
  }

  return <div>Loading...</div>;
}

// -------------------------------------------------------
// Reusable Components
// -------------------------------------------------------
function DashButton({ label, onClick, color }) {
  return (
    <button
      onClick={onClick}
      className={`
        bg-gradient-to-r ${color}
        text-white py-3 rounded-xl text-lg font-semibold
        shadow-md border border-white/30
        transition-all duration-200
        hover:shadow-xl hover:scale-[1.02]
        active:scale-95
      `}
    >
      {label}
    </button>
  );
}

function DashboardSection({ title, setView, children }) {
  return (
    <div
      className="min-h-screen bg-cover bg-center p-10"
      style={{ backgroundImage: "url('/background.png')" }}
    >
      <div className="bg-white/30 backdrop-blur-md border border-white/40 p-8 max-w-3xl mx-auto rounded-2xl shadow-xl">
        <h1 className="text-3xl font-bold text-white drop-shadow mb-6">
          {title}
        </h1>

        <button
          onClick={() => setView("home")}
          className="mb-5 bg-purple-700 text-white px-5 py-2 rounded shadow hover:bg-purple-800 transition"
        >
          ⬅ Back to Dashboard
        </button>

        {children}
      </div>
    </div>
  );
}
