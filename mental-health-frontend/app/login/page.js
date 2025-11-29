"use client";
import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";

export default function LoginPage() {
  const router = useRouter();
  const [form, setForm] = useState({ email: "", password: "", role: "patient" });
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    localStorage.clear();
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError("");

    try {
      const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/auth/login`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(form),
      });

      const data = await res.json();
      setLoading(false);

      if (!res.ok) throw new Error(data.detail || "Login failed");

      // Store items
      localStorage.setItem("token", data.access_token);
      localStorage.setItem("role", form.role);
      localStorage.setItem("user_id", data.user_id);

      if (form.role === "doctor") {
        localStorage.setItem("doctor_id", data.user_id);
        router.push("/dashboard/doctor");
      } else if (form.role === "admin") {
        router.push("/dashboard/admin");
      } else {
        router.push("/dashboard/patient");
      }

    } catch (err) {
      setError(err.message);
      setLoading(false);
    }
  };

  return (
    <div
      className="min-h-screen flex items-center justify-center bg-cover bg-center p-6"
      style={{ backgroundImage: "url('/background.png')" }}
    >
      <form
        onSubmit={handleSubmit}
        className="bg-white/40 backdrop-blur-xl shadow-2xl rounded-2xl p-10 w-full max-w-md border border-white/60 animate-fadeIn"
      >
        {/* MindConnect Logo */}
        <div className="flex justify-center mb-6">
          <img
            src="/mindconnect-logo.png"
            alt="MindConnect"
            className="w-40 h-auto object-contain drop-shadow-lg"
            onError={(e) => {
              e.currentTarget.style.display = "none";
            }}
          />
        </div>

        {/* Text fallback if logo not found */}
        <h1 className="text-4xl font-extrabold text-center mb-4 text-blue-800 drop-shadow">
          MindConnect
        </h1>

        {error && (
          <p className="text-red-600 bg-red-100 p-2 rounded text-center mb-4">
            {error}
          </p>
        )}

        {/* Email */}
        <label className="block mb-4">
          <span className="font-semibold text-gray-900">Email</span>
          <input
            type="email"
            className="border border-gray-300 bg-white rounded w-full p-3 mt-1 focus:ring-2 focus:ring-blue-500 outline-none"
            value={form.email}
            onChange={(e) => setForm({ ...form, email: e.target.value })}
            required
          />
        </label>

        {/* Password */}
        <label className="block mb-4">
          <span className="font-semibold text-gray-900">Password</span>
          <input
            type="password"
            className="border border-gray-300 bg-white rounded w-full p-3 mt-1 focus:ring-2 focus:ring-blue-500 outline-none"
            value={form.password}
            onChange={(e) => setForm({ ...form, password: e.target.value })}
            required
          />
        </label>

        {/* Role */}
        <label className="block mb-6">
          <span className="font-semibold text-gray-900">Select Role</span>
          <select
            className="border border-gray-300 bg-white rounded w-full p-3 mt-1 focus:ring-2 focus:ring-blue-500 outline-none"
            value={form.role}
            onChange={(e) => setForm({ ...form, role: e.target.value })}
          >
            <option value="patient">Patient</option>
            <option value="doctor">Doctor</option>
            <option value="admin">Admin</option>
          </select>
        </label>

        {/* Login Button */}
        <button
          type="submit"
          className="w-full bg-blue-600 text-white py-3 rounded-xl font-semibold text-lg shadow-md hover:bg-blue-700 active:scale-95 transition-all duration-200"
          disabled={loading}
        >
          {loading ? "Logging in..." : "Login"}
        </button>

        {/* Register Link */}
        <p className="text-center text-gray-900 mt-5 text-sm">
          Don’t have an account?{" "}
          <a
            href="/register"
            className="text-blue-700 font-semibold hover:underline transition"
          >
            Register here
          </a>
        </p>
      </form>

      {/* Fade animation */}
      <style>{`
        .animate-fadeIn {
          animation: fadeIn 1s ease-in-out;
        }
        @keyframes fadeIn {
          from { opacity: 0; transform: translateY(10px); }
          to { opacity: 1; transform: translateY(0); }
        }
      `}</style>
    </div>
  );
}
