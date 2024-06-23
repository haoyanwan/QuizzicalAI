// Home.jsx
"use client";

import React, { useState, useEffect } from 'react';
import axios from 'axios';
import QuizPrompt from "./component/quizprompt";
import AnswerBox from "./component/answerbbox";

const Home = () => {
  const [questionData, setQuestionData] = useState(null);
  const [loading, setLoading] = useState(true);

  const fetchQuestion = async () => {
    setLoading(true);
    try {
      const response = await axios.get('/api/generate_question');
      setQuestionData(response.data);
    } catch (error) {
      console.error('Error fetching question:', error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchQuestion();
  }, []);

  return (
    <div
      className="relative mx-2 my-2 bg-f5f5f5 rounded-2xl overflow-hidden"
      style={{
        height: "calc(100vh - 15px)", // Keep dynamic height calculation in inline style
        width: "calc(100% - 15px)", // Keep dynamic width calculation in inline style
      }}
    >
      {/* Top Left Container absolutely positioned */}
      <div
        className="absolute left-0 top-0 p-3 bg-white rounded-lg"
        style={{
          width: "38%",
          height: "29.5%",
          margin: "1%",
        }}
      >
        {/* Content for top left box */}
      </div>

      {/* Top Right Container absolutely positioned */}
      <div
        className="absolute right-0 top-0 p-3 bg-white rounded-lg"
        style={{
          width: "58%",
          height: "29.5%",
          margin: "1%",
        }}
      >
        {/* Content for top right box */}
      </div>

      {/* Bottom Left Container absolutely positioned */}
      <div
        className="absolute left-0 bottom-0 p-3 bg-white rounded-lg"
        style={{
          width: "28%",
          height: "64.4%",
          margin: "1%",
        }}
      >
        {/* Content for bottom left box */}
      </div>

      {/* Bottom Right Container absolutely positioned */}
      <div
        className="absolute right-0 bottom-0 p-3 bg-white rounded-lg"
        style={{
          width: "68%",
          height: "64.4%",
          margin: "1%",
        }}
      >
        <h2 className="p-6 pb-0 text-2xl font-bold mb-4 text-blue-800">Questions</h2>
        <QuizPrompt questionData={questionData} loading={loading} />
        <AnswerBox questionData={questionData} fetchQuestion={fetchQuestion} />
      </div>
    </div>
  );
};

export default Home;
