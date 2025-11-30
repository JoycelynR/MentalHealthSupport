"use client";
import { useEffect, useState } from "react";

export default function AdminDashboard() {
  const [data, setData] = useState(null);
  const [error, setError] = useState("");
  const [view, setView] = useState("home"); // home | addDoctor | listDoctors | deleteDoctor
  const [doctors, setDoctors] = useState([]);
  const [newDoctor, setNewDoctor] = useState({
    name: "",
    email: "",
    password: "",
  });
  const [deleteId, setDeleteId] = useState("");

  const apiUrl = process.env.NEXT_PUBLIC_API_URL;
  const token = typeof window !== "undefined" ? localStorage.getItem("token") : null;

  useEffect(() => {
    if (!token) {
      setError("You are not logged in.");
      return;
    }
    loadDashboardStats();
  }, []);

  // Fetch admin stats
  async function loadDashboardStats() {
    try {
      const res = await fetch(`${apiUrl}/admin/dashboard`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      if (!res.ok) throw new Error("Failed to load dashboard");
      setData(await res.json());
    } catch (err) {
      setError(err.message);
    }
  }

  // Fetch doctors list
  async function loadDoctors() {
    try {
      const res = await fetch(`${apiUrl}/doctors/`);
      if (!res.ok) throw new Error("Failed to load doctors");
      setDoctors(await res.json());
      setView("listDoctors");
    } catch (err) {
      setError(err.message);
    }
  }

  // Add doctor
  async function submitDoctor() {
    try {
      const res = await fetch(`${apiUrl}/doctors/`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(newDoctor),
      });
      if (!res.ok) throw new Error("Failed to create doctor");
      alert("Doctor added successfully");
      setNewDoctor({ name: "", email: "", specialization: "", password: "" });
      setView("home");
    } catch (err) {
      alert(err.message);
    }
  }

  // Delete doctor
  async function submitDelete() {
    try {
      const res = await fetch(`${apiUrl}/doctors/${deleteId}`, {
        method: "DELETE",
      });
      if (!res.ok) throw new Error("Doctor not found");
      alert("Doctor deleted");
      setDeleteId("");
      setView("home");
    } catch (err) {
      alert(err.message);
    }
  }

  if (error) return <p className="text-red-500 p-10 text-center">{error}</p>;
  if (!data) return <p className="text-center p-10">Loading...</p>;

  // =========================
  // HOME VIEW
  // =========================
  if (view === "home") {
    return (
      <div
        className="min-h-screen bg-cover bg-center p-10"
        style={{ backgroundImage: "url('/background.png')" }}
      >
        <div className="bg-white/70 backdrop-blur-md p-8 rounded-2xl shadow-xl max-w-3xl mx-auto">
          <div className="flex justify-between items-center mb-6">
            <h1 className="text-3xl font-bold text-blue-900">Admin Dashboard</h1>

            <button
              className="bg-red-500 text-white px-4 py-2 rounded hover:bg-red-600"
              onClick={() => {
                localStorage.clear();
                window.location.href = "/login";
              }}
            >
              Logout
            </button>
          </div>

          <div className="space-y-3 text-lg">
            <p><strong>Total Users:</strong> {data.users_count}</p>
            <p><strong>Total Doctors:</strong> {data.doctors_count}</p>
            <p><strong>Total Consultations:</strong> {data.consultations_count}</p>
          </div>

          {/* Admin Actions */}
          <div className="mt-8 grid grid-cols-1 md:grid-cols-2 gap-4">
            <button
              onClick={() => setView("addDoctor")}
              className="bg-blue-600 text-white py-3 rounded-lg hover:bg-blue-700"
            >
              ➕ Add Doctor
            </button>
            <button
              onClick={loadDoctors}
              className="bg-indigo-600 text-white py-3 rounded-lg hover:bg-indigo-700"
            >
              📋 View Doctors
            </button>
            <button
              onClick={() => setView("deleteDoctor")}
              className="bg-red-600 text-white py-3 rounded-lg hover:bg-red-700"
            >
              ❌ Delete Doctor
            </button>
          </div>
        </div>
      </div>
    );
  }

  // =========================
  // ADD DOCTOR VIEW
  // =========================
  if (view === "addDoctor") {
    return (
      <AdminSection title="Add Doctor" setView={setView}>
        <input
          className="w-full p-2 border rounded mb-3"
          placeholder="Name"
          value={newDoctor.name}
          onChange={(e) => setNewDoctor({ ...newDoctor, name: e.target.value })}
        />
        <input
          className="w-full p-2 border rounded mb-3"
          placeholder="Email"
          value={newDoctor.email}
          onChange={(e) => setNewDoctor({ ...newDoctor, email: e.target.value })}
        />
        <input
          className="w-full p-2 border rounded mb-3"
          type="password"
          placeholder="Password"
          value={newDoctor.password}
          onChange={(e) =>
            setNewDoctor({ ...newDoctor, password: e.target.value })
          }
        />

        <button
          onClick={submitDoctor}
          className="bg-blue-600 text-white w-full py-3 rounded-lg hover:bg-blue-700"
        >
          Add Doctor
        </button>
      </AdminSection>
    );
  }

  // =========================
  // LIST DOCTORS VIEW
  // =========================
  if (view === "listDoctors") {
    return (
      <AdminSection title="Doctors List" setView={setView}>
        {doctors.map((d) => (
          <div key={d.id} className="bg-white/70 p-4 rounded shadow mb-3">
            <p><strong>Name:</strong> {d.name}</p>
            <p><strong>Email:</strong> {d.email}</p>
          </div>
        ))}
      </AdminSection>
    );
  }

  // =========================
  // DELETE DOCTOR VIEW
  // =========================
  if (view === "deleteDoctor") {
    return (
      <AdminSection title="Delete Doctor" setView={setView}>
        <input
          placeholder="Doctor ID"
          className="w-full p-2 border rounded mb-3"
          value={deleteId}
          onChange={(e) => setDeleteId(e.target.value)}
        />

        <button
          onClick={submitDelete}
          className="bg-red-600 text-white w-full py-3 rounded-lg hover:bg-red-700"
        >
          Delete
        </button>
      </AdminSection>
    );
  }

  return <div>Loading...</div>;
}

// ========================================================
// REUSABLE WRAPPER
// ========================================================
function AdminSection({ title, setView, children }) {
  return (
    <div
      className="min-h-screen bg-cover bg-center p-10"
      style={{ backgroundImage: "url('/background.png')" }}
    >
      <div className="bg-white/70 backdrop-blur-md p-8 rounded-2xl shadow-xl max-w-3xl mx-auto">
        <h1 className="text-3xl font-bold text-blue-900 mb-6">{title}</h1>

        <button
          onClick={() => setView("home")}
          className="mb-5 bg-gray-700 text-white px-4 py-2 rounded hover:bg-gray-800"
        >
          ⬅ Back
        </button>

        {children}
      </div>
    </div>
  );
}
