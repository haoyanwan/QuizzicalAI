"use client";
import React, { useState, useEffect } from "react";
import axios from "axios";
import QuizPrompt from "../component/quizprompt";
import AnswerBox from "../component/answerbox";
import LearningObjectiveChart from "../component/LearningObjectiveChart";
import RecentPerformanceChart from "../component/performancchart";
import AssessmentBox from "../component/assesmentbox";
import CourseContentDive from "../component/coursecontentdive"; // Import the CourseContentDive component

const Home = () => {
  const [questionData, setQuestionData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [refresh, setRefresh] = useState(false);
  const [updateAssessment, setUpdateAssessment] = useState(false);

  const fetchQuestion = async () => {
    setLoading(true);
    try {
      const response = await axios.get("/api/generate_question");
      setQuestionData(response.data);
    } catch (error) {
      console.error("Error fetching question:", error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchQuestion();
  }, []);

  const triggerRefresh = () => {
    setRefresh((prev) => !prev);
  };

  const handleAnswerSubmit = () => {
    setUpdateAssessment((prev) => !prev); // Trigger re-fetch of assessment data
  };

  return (
    <div
      className="relative mx-2 my-2 bg-f5f5f5 rounded-2xl overflow-hidden"
      style={{
        height: "calc(100vh - 5px)", // Keep dynamic height calculation in inline style
        width: "calc(100% - 15px)", // Keep dynamic width calculation in inline style
      }}
    >
      {/* Top Right Container for Recent Performance */}
      <div
        className="absolute right-0 top-0 p-3 bg-white rounded-lg"
        style={{ width: "59%", height: "30%", margin: "1%" }}
      >
        <RecentPerformanceChart />
        <div className="absolute top-2 right-2 h-[92%] w-[38%] bg-gray-100 rounded-lg p-2">
          <AssessmentBox updateAssessment={updateAssessment} />{" "}
          {/* Pass the updateAssessment state */}
        </div>
      </div>

      {/* Top Left Container absolutely positioned */}
      <div
        className="absolute left-0 top-0 p-3 bg-white rounded-lg"
        style={{
          width: "38%",
          height: "29.5%",
          margin: "1%",
        }}
      >
        <div className="max-w-sm rounded overflow-hidden flex">
          <img
            className="w-7/12"
            src="/img/logo.png"
            alt="AP Environmental Science"
          />
          <div className="px-2 py-2 flex flex-col justify-center">
            <div className="font-bold text-lg mb-1">AP Environmental Science</div>
            <p className="text-gray-700 text-sm">
              Explore the impact of human activities on the environment and
              learn sustainable practices.
            </p>
          </div>
        </div>
      </div>

      {/* Bottom Left Container for Curriculum Progress */}
      <div
        className="absolute left-0 bottom-14 p-2 bg-white rounded-lg"
        style={{
          width: "28%",
          height: "58.4%",
          margin: "1%",
        }}
      >
        <LearningObjectiveChart refresh={refresh} />
      </div>

      {/* Bottom Right Container absolutely positioned */}
      <div
        className="absolute right-0 bottom-14 p-2 bg-white rounded-lg flex flex-col justify-between"
        style={{
          width: "68%",
          height: "58.4%",
          margin: "1%",
        }}
      >
        <CourseContentDive /> {/* Add the CourseContentDive component here */}
      </div>
    </div>
  );
};

export default Home;
