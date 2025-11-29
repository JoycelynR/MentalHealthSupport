"use client";
import { useState,useEffect } from "react";

export default function AssessmentForm() {
  const [mood, setMood] = useState(5);
  const [energy, setEnergy] = useState(3);
  const [focus, setFocus] = useState(3);
  const [sleep, setSleep] = useState(3);
  const [positive, setPositive] = useState([]);
  const [negative, setNegative] = useState([]);
  const [result, setResult] = useState(null);
  const [userId, setUserId] = useState(null);
const [loading, setLoading] = useState(false);
const [formData, setFormData] = useState({
  moodRating: 5,
});
  const apiUrl = process.env.NEXT_PUBLIC_API_URL;
  useEffect(() => {
    const id = localStorage.getItem("user_id");
    setUserId(id);
  }, []);

  const toggleSelection = (list, setList, value) => {
    setList(list.includes(value) ? list.filter(i => i !== value) : [...list, value]);
  };

const handleSubmit = async (e) => {
  e.preventDefault();
  setLoading(true);
  setResult(null);

  try {
    const raw = Number(formData.moodRating || 5); // get value from your form
    const mood_score = Math.min(Math.max(raw, 1), 10);

    const res = await fetch(`${apiUrl}/assessments/`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        user_id: userId,
        mood_score,
      }),
    });

    const data = await res.json();
    console.log("Response data:", data);

    setResult({
      score: data.mood_score ?? data.score ?? "N/A",
      recommendation: data.recommendation ?? "No recommendation returned",
    });
  } catch (err) {
    console.error(err);
    alert("Error submitting assessment");
  } finally {
    setLoading(false);
  }
};  

  return (
    <div className="max-w-3xl mx-auto bg-white shadow-lg p-6 mt-10 rounded-lg">
      <h1 className="text-2xl font-bold mb-6 text-center">Mood Assessment</h1>
      <form onSubmit={handleSubmit} className="space-y-6">

        {/* Part 1 */}
        <div>
          <h2 className="font-semibold mb-2">1. Rate your overall emotional state</h2>
          <input type="range" min="1" max="10" value={mood}
            onChange={e => setMood(e.target.value)} className="w-full" />
          <p className="text-center text-sm mt-1">Current: {mood}/10</p>
        </div>

        {/* Part 2 - Energy */}
        <div>
          <h2 className="font-semibold mb-2">2. Energy level today</h2>
          {[1,2,3,4,5].map(i => (
            <label key={i} className="mr-3">
              <input type="radio" value={i} checked={energy==i} onChange={()=>setEnergy(i)} /> {i}
            </label>
          ))}
        </div>

        {/* Focus */}
        <div>
          <h2 className="font-semibold mb-2">3. Focus today</h2>
          {[1,2,3,4,5].map(i => (
            <label key={i} className="mr-3">
              <input type="radio" value={i} checked={focus==i} onChange={()=>setFocus(i)} /> {i}
            </label>
          ))}
        </div>

        {/* Part 3 - Positive */}
        <div>
          <h2 className="font-semibold mb-2">4. Positive feelings today</h2>
          {["Joyful","Calm","Content","Interested","Loving"].map(f => (
            <label key={f} className="block">
              <input type="checkbox" checked={positive.includes(f)}
                onChange={() => toggleSelection(positive, setPositive, f)} /> {f}
            </label>
          ))}
        </div>

        {/* Negative feelings */}
        <div>
          <h2 className="font-semibold mb-2">5. Negative feelings today</h2>
          {["Anxious","Irritable","Sad","Hopeless","Stressed"].map(f => (
            <label key={f} className="block">
              <input type="checkbox" checked={negative.includes(f)}
                onChange={() => toggleSelection(negative, setNegative, f)} /> {f}
            </label>
          ))}
        </div>

        {/* Part 4 - Sleep */}
        <div>
          <h2 className="font-semibold mb-2">6. How was your sleep?</h2>
          {[1,2,3,4,5].map(i => (
            <label key={i} className="mr-3">
              <input type="radio" value={i} checked={sleep==i} onChange={()=>setSleep(i)} /> {i}
            </label>
          ))}
        </div>

        <button className="bg-blue-600 text-white px-6 py-2 rounded hover:bg-blue-700">
          Submit
        </button>
      </form>

      {result && (
        <div className="mt-6 bg-green-50 p-4 rounded">
          <h3 className="font-bold text-lg mb-2">Result</h3>
          <p><strong>Score:</strong> {result.score}</p>
          <p><strong>Recommendation:</strong> {result.recommendation}</p>
        </div>
      )}
    </div>
  );
}
