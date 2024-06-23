"use client";

import React from 'react';

const QuizPrompt = ({ questionData, loading }) => {
  if (loading) {
    return (
      <div className="max-w-4xl mx-auto flex justify-center items-center">
        <div className="spinner-border animate-spin inline-block w-8 h-8 border-4 rounded-full" role="status">
          <span className="visually-hidden"></span>
        </div>
      </div>
    );
  }

  if (!questionData) {
    return (
      <div className="max-w-4xl mx-auto">
        <div className="rounded-lg pl-4">
          <div>
            <p className="text-base ml-2 font-medium text-red-500">Failed to load question. Please try again later.</p>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-4xl mx-auto">
      <div className="rounded-lg pl-4">
        <div>
          <p className="text-base ml-2 font-medium">{questionData.question}</p>
        </div>
      </div>
    </div>
  );
};

export default QuizPrompt;
