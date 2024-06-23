// AnswerBox.jsx
import React, { useState } from 'react';
import axios from 'axios';

const AnswerBox = ({ questionData, fetchQuestion }) => {
  const [answer, setAnswer] = useState('');

  const handleSubmit = async () => {
    if (!answer.trim()) return;

    try {
      const response = await axios.post('/api/grade_answer', {
        question: questionData.question,
        answer: answer.trim(),
        essential_knowledge_code: questionData.essential_knowledge_code,
      });
      console.log('Grading result:', response.data);
    } catch (error) {
      console.error('Error grading answer:', error);
    } finally {
      setAnswer('');
      fetchQuestion();
    }
  };

  return (
    <div className="ml-6 mt-5">
      <label htmlFor="answer" className="block mb-2 text-sm font-medium text-gray-900 dark:text-white">
        Your Answer
      </label>
      <textarea
        id="answer"
        rows="4"
        className="block p-2.5 w-full text-sm text-gray-900 bg-gray-50 rounded-lg border border-gray-300 focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
        placeholder="Write your answer here..."
        value={answer}
        onChange={(e) => setAnswer(e.target.value)}
      ></textarea>
      <button
        className="mt-4 flex items-center px-4 py-2 bg-blue-600 text-white text-sm font-medium rounded-lg hover:bg-blue-700 focus:ring-4 focus:ring-blue-300 transition duration-200"
        onClick={handleSubmit}
      >
        <svg className="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 13l4 4L19 7"></path>
        </svg>
        Submit
      </button>
    </div>
  );
};

export default AnswerBox;
