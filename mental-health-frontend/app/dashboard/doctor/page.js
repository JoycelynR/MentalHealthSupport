"use client";
import { useEffect, useState } from "react";

export default function DoctorDashboard() {
  const [consultations, setConsultations] = useState([]);
  const [selectedPatient, setSelectedPatient] = useState(null);
  const [newNote, setNewNote] = useState("");
  const [prescription, setPrescription] = useState({
    medication: "",
    dosage: "",
    instructions: "",
  });

  const apiUrl = process.env.NEXT_PUBLIC_API_URL;
  const token =
    typeof window !== "undefined" ? localStorage.getItem("token") : null;

  // Doctor ID from login
  const doctorId =
    typeof window !== "undefined"
      ? localStorage.getItem("doctor_id") || localStorage.getItem("user_id")
      : null;

  // ------------------------------------------------------
  // Fetch Assigned Consultations
  // ------------------------------------------------------
  const fetchConsultations = async () => {
    if (!doctorId) return;

    try {
      const res = await fetch(`${apiUrl}/consultations/doctor/${doctorId}`, {
        headers: { Authorization: `Bearer ${token}` },
      });

      if (!res.ok) {
        setConsultations([]);
        return;
      }

      const data = await res.json();
      setConsultations(Array.isArray(data) ? data : []);
    } catch (err) {
      console.error("Fetch error:", err);
    }
  };

  useEffect(() => {
    fetchConsultations();
  }, [doctorId]);

  // ------------------------------------------------------
  // LOAD PATIENT ASSESSMENTS WHEN CLICKED
  // ------------------------------------------------------
  const openPatientDetails = async (consultation) => {
    try {
      const res = await fetch(
        `${apiUrl}/assessments/user/${consultation.user_id}`,
        {
          headers: { Authorization: `Bearer ${token}` },
        }
      );

      const assessments = await res.json();

      setSelectedPatient({
        ...consultation,
        assessments: Array.isArray(assessments) ? assessments : [],
      });
    } catch (error) {
      console.error("Error loading assessments:", error);
    }
  };

  // ------------------------------------------------------
  // Save Notes
  // ------------------------------------------------------
  const saveNote = async (consultationId) => {
    try {
      const res = await fetch(`${apiUrl}/consultations/${consultationId}/notes`, {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({ notes: newNote }),
      });

      if (res.ok) {
        alert("Note saved successfully!");
        setNewNote("");
        fetchConsultations();
      } else {
        alert("Failed to save note.");
      }
    } catch (err) {
      console.error(err);
    }
  };

  // ------------------------------------------------------
  // Add Prescription
  // ------------------------------------------------------
  const handleAddPrescription = async (consultationId) => {
    try {
      const res = await fetch(
        `${apiUrl}/consultations/${consultationId}/prescription`,
        {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            consultation_id: consultationId,
            medication: prescription.medication,
            dosage: prescription.dosage,
            instructions: prescription.instructions,
            pharmacy_id: 1,
          }),
        }
      );

      if (res.ok) {
        alert("Prescription added!");
        setPrescription({ medication: "", dosage: "", instructions: "" });
      } else {
        alert("Failed to add prescription");
      }
    } catch (err) {
      console.error(err);
    }
  };

  // ------------------------------------------------------
  // UI
  // ------------------------------------------------------
  return (
    <div
      className="min-h-screen bg-cover bg-center p-10 flex justify-center"
      style={{ backgroundImage: "url('/background.png')" }}
    >
      <div className="bg-white/85 backdrop-blur-xl p-8 rounded-2xl shadow-xl w-full max-w-6xl">
        <h1 className="text-3xl font-bold text-center text-blue-800 mb-6">
          MindConnect — Doctor Dashboard
        </h1>

        {/* TABLE OF PATIENTS */}
        <table className="w-full border border-gray-300 text-sm mb-8">
          <thead>
            <tr className="bg-blue-50 text-left font-semibold text-gray-700">
              <th className="p-3">Patient Name</th>
              <th className="p-3">Date</th>
              <th className="p-3">Notes</th>
              <th className="p-3 text-center">Actions</th>
            </tr>
          </thead>
          <tbody>
            {consultations.length > 0 ? (
              consultations.map((c, i) => (
                <tr key={i} className="border-t hover:bg-blue-50/40 transition">
                  <td className="p-3">{c.patient_name}</td>
                  <td className="p-3">
                    {new Date(c.date).toLocaleDateString()}
                  </td>
                  <td className="p-3">{c.notes || "No notes yet"}</td>
                  <td className="p-3 text-center">
                    <button
                      className="bg-blue-600 text-white px-4 py-1 rounded-lg hover:bg-blue-700 transition"
                      onClick={() => openPatientDetails(c)}
                    >
                      View Details
                    </button>
                  </td>
                </tr>
              ))
            ) : (
              <tr>
                <td
                  colSpan="4"
                  className="text-center p-4 text-gray-500 italic"
                >
                  No patients assigned.
                </td>
              </tr>
            )}
          </tbody>
        </table>

        {/* PATIENT DETAILS MODAL */}
        {selectedPatient && (
          <div className="bg-white border rounded-xl p-6 shadow-xl mt-8">
            <h2 className="text-2xl font-bold text-blue-700 mb-4">
              Patient: {selectedPatient.patient_name}
            </h2>

            {/* ASSESSMENT HISTORY */}
            <h3 className="text-lg font-semibold mt-4 mb-2">Assessment History</h3>
            {selectedPatient.assessments.length > 0 ? (
              selectedPatient.assessments.map((a, i) => (
                <div
                  key={i}
                  className="border p-3 rounded-lg bg-gray-50 mb-3 shadow-sm"
                >
                  <p>
                    <strong>Date:</strong>{" "}
                    {new Date(a.created_at).toLocaleString()}
                  </p>
                  <p>
                    <strong>Mood Score:</strong> {a.mood_score}
                  </p>
                  <p>
                    <strong>Recommendation:</strong> {a.recommendation}
                  </p>
                </div>
              ))
            ) : (
              <p className="text-gray-600">No assessments found.</p>
            )}

            {/* NOTES */}
            <textarea
              placeholder="Add or update note..."
              value={newNote}
              onChange={(e) => setNewNote(e.target.value)}
              className="w-full border rounded-lg p-3 mt-4"
            />
            <button
              className="bg-green-600 text-white px-4 py-2 rounded-lg mt-2 hover:bg-green-700 transition"
              onClick={() => saveNote(selectedPatient.id)}
            >
              Save Note
            </button>

            {/* PRESCRIPTION */}
            <div className="mt-6">
              <h3 className="text-lg font-semibold mb-2">Add Prescription</h3>

              <input
                type="text"
                placeholder="Medication"
                className="w-full border p-2 rounded mb-2"
                value={prescription.medication}
                onChange={(e) =>
                  setPrescription({ ...prescription, medication: e.target.value })
                }
              />

              <input
                type="text"
                placeholder="Dosage"
                className="w-full border p-2 rounded mb-2"
                value={prescription.dosage}
                onChange={(e) =>
                  setPrescription({ ...prescription, dosage: e.target.value })
                }
              />

              <textarea
                placeholder="Instructions"
                className="w-full border p-2 rounded mb-2"
                value={prescription.instructions}
                onChange={(e) =>
                  setPrescription({
                    ...prescription,
                    instructions: e.target.value,
                  })
                }
              />

              <button
                className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700"
                onClick={() => handleAddPrescription(selectedPatient.id)}
              >
                Add Prescription
              </button>

              <button
                className="ml-3 bg-gray-600 text-white px-4 py-2 rounded-lg hover:bg-gray-700"
                onClick={() => setSelectedPatient(null)}
              >
                Close
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
