import React, { useState } from "react";
import axios from "axios";
import { FaPaperPlane } from "react-icons/fa";

const AnswerBox = ({ questionData, fetchQuestion, triggerRefresh, onAnswerSubmit }) => {
  const [answer, setAnswer] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (event) => {
    event.preventDefault();
    setLoading(true);

    try {
      await axios.post("/api/grade_answer", {
        question: questionData.question,
        answer: answer,
        essential_knowledge_code: questionData.essential_knowledge_code,
      });
      fetchQuestion();
      triggerRefresh();
      onAnswerSubmit(); // Trigger the callback to update the assessment box
    } catch (error) {
      console.error("Error submitting answer:", error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <textarea
        value={answer}
        onChange={(e) => setAnswer(e.target.value)}
        placeholder="Type your answer here..."
        className="w-full p-2 border rounded-md"
      />
      <button
        type="submit"
        className={`mt-2 px-4 py-2 bg-blue-500 text-white rounded-md flex items-center justify-center transition duration-300 ease-in-out transform ${
          loading ? "opacity-50 cursor-not-allowed" : "hover:bg-blue-600 hover:scale-105"
        }`}
        disabled={loading}
      >
        {loading ? (
          <svg className="animate-spin h-5 w-5 mr-3" viewBox="0 0 24 24">
            <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
            <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C6.28 0 0 6.28 0 14h4z"></path>
          </svg>
        ) : (
          <FaPaperPlane className="mr-2" />
        )}
        {loading ? "Submitting..." : "Submit"}
      </button>
    </form>
  );
};

export default AnswerBox;
