import React, { useEffect, useState } from "react";
import axios from "axios";

const AssessmentBox = ({ updateAssessment }) => {
  const [assessmentData, setAssessmentData] = useState({ strengths: [], weaknesses: [], habits: [] });

  const fetchAssessmentData = async () => {
    try {
      const response = await axios.get("/api/latest_assessment");
      setAssessmentData(response.data);
    } catch (error) {
      console.error("Error fetching assessment data:", error);
    }
  };

  useEffect(() => {
    fetchAssessmentData();
  }, [updateAssessment]); // Re-fetch assessment data when updateAssessment changes

  return (
    <div className="p-2">
      <h3 className="text-sm font-semibold mb-2 text-blue-800">Latest Assessment</h3>
      <div className="mb-1">
        <strong className="text-xs font-semibold text-gray-600">Strengths:</strong>
        <ul className="list-disc list-inside text-xs text-gray-600 space-y-1">
          {assessmentData.strengths.map((strength, index) => (
            <li key={index}>{strength}</li>
          ))}
        </ul>
      </div>
      <div className="mb-1">
        <strong className="text-xs font-semibold text-gray-600">Weaknesses:</strong>
        <ul className="list-disc list-inside text-xs text-gray-600 space-y-1">
          {assessmentData.weaknesses.map((weakness, index) => (
            <li key={index}>{weakness}</li>
          ))}
        </ul>
      </div>
      <div className="mb-1">
        <strong className="text-xs font-semibold text-gray-600">Habits:</strong>
        <ul className="list-disc list-inside text-xs text-gray-600 space-y-1">
          {assessmentData.habits.map((habit, index) => (
            <li key={index}>{habit}</li>
          ))}
        </ul>
      </div>
    </div>
  );
};

export default AssessmentBox;
