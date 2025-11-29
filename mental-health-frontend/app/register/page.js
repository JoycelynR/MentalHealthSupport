"use client";
import { useState } from "react";
import { useRouter } from "next/navigation";

export default function RegisterPage() {
  const router = useRouter();
  const [form, setForm] = useState({ name: "", email: "", password: "" });
  const [message, setMessage] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();

    const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/users/register`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(form),
    });

    const data = await res.json();

    if (res.ok) {
      setMessage("Registration successful! Redirecting...");
      setTimeout(() => router.push("/login"), 1500);
    } else {
      setMessage(data.detail || "Registration failed.");
    }
  };

  return (
    <div
      className="min-h-screen flex items-center justify-center bg-center bg-cover p-6"
      style={{ backgroundImage: "url('/background.png')" }}
    >
      <form
        onSubmit={handleSubmit}
        className="bg-white/80 backdrop-blur-lg shadow-xl rounded-xl p-8 w-full max-w-md animate-fadeIn"
      >
        <h2 className="text-3xl font-bold text-center mb-6 text-blue-700 drop-shadow">
          Create Patient Account
        </h2>

        <input
          type="text"
          placeholder="Name"
          className="w-full border p-2 rounded mb-3 focus:ring focus:ring-blue-300 transition"
          value={form.name}
          onChange={(e) => setForm({ ...form, name: e.target.value })}
          required
        />

        <input
          type="email"
          placeholder="Email"
          className="w-full border p-2 rounded mb-3 focus:ring focus:ring-blue-300 transition"
          value={form.email}
          onChange={(e) => setForm({ ...form, email: e.target.value })}
          required
        />

        <input
          type="password"
          placeholder="Password"
          className="w-full border p-2 rounded mb-4 focus:ring focus:ring-blue-300 transition"
          value={form.password}
          onChange={(e) => setForm({ ...form, password: e.target.value })}
          required
        />

        <button
          type="submit"
          className="w-full bg-green-600 text-white py-2 rounded-lg font-semibold hover:bg-green-700 hover:scale-[1.02] active:scale-[0.98] transition-transform shadow"
        >
          Register
        </button>

        {message && (
          <p className="text-center mt-3 text-sm text-gray-700">{message}</p>
        )}

        <p className="text-center mt-4 text-gray-700">
          Already have an account?{" "}
          <span
            onClick={() => router.push("/login")}
            className="text-blue-700 font-semibold hover:underline cursor-pointer"
          >
            Login
          </span>
        </p>
      </form>
    </div>
  );
}
