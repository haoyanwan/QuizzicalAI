import React, { useEffect, useState } from 'react';
import axios from 'axios';

const getColor = (index) => {
  const colors = [
    'bg-red-500', 
    'bg-blue-500', 
    'bg-green-500', 
    'bg-yellow-500', 
    'bg-purple-500', 
    'bg-pink-500', 
    'bg-indigo-500', 
    'bg-teal-500', 
    'bg-orange-500', 
    'bg-gray-500'
  ];
  return colors[index % colors.length];
};

const getLighterColor = (color) => {
  const colorMap = {
    'bg-red-500': 'bg-red-100',
    'bg-blue-500': 'bg-blue-100',
    'bg-green-500': 'bg-green-100',
    'bg-yellow-500': 'bg-yellow-100',
    'bg-purple-500': 'bg-purple-100',
    'bg-pink-500': 'bg-pink-100',
    'bg-indigo-500': 'bg-indigo-100',
    'bg-teal-500': 'bg-teal-100',
    'bg-orange-500': 'bg-orange-100',
    'bg-gray-500': 'bg-gray-100',
  };
  return colorMap[color] || 'bg-gray-100';
};

const getMediumColor = (color) => {
  const colorMap = {
    'bg-red-500': 'bg-red-300',
    'bg-blue-500': 'bg-blue-300',
    'bg-green-500': 'bg-green-300',
    'bg-yellow-500': 'bg-yellow-300',
    'bg-purple-500': 'bg-purple-300',
    'bg-pink-500': 'bg-pink-300',
    'bg-indigo-500': 'bg-indigo-300',
    'bg-teal-500': 'bg-teal-300',
    'bg-orange-500': 'bg-orange-300',
    'bg-gray-500': 'bg-gray-300',
  };
  return colorMap[color] || 'bg-gray-300';
};

const LearningObjectiveChart = ({ refresh }) => {
  const [data, setData] = useState([]);

  const fetchData = async () => {
    try {
      const response = await axios.get('/api/learning_objectives_scores');
      setData(response.data);
    } catch (error) {
      console.error('Error fetching data:', error);
    }
  };

  useEffect(() => {
    fetchData();
  }, [refresh]);

  return (
    <div className="flex flex-col items-center w-full p-2">
      <h2 className="text-2xl font-bold mb-2 text-blue-800">Curriculum Progress</h2>
      <div className="flex flex-col gap-2 w-full max-w-4xl">
        <div className="flex items-center justify-between w-full">
          <div className="text-center text-gray-500 text-xs w-1/5">Topic</div>
          <div className="text-left text-gray-500 text-xs w-3/4"></div>
          <div className="text-right text-gray-500 text-xs w-16">Progress</div>
        </div>
        {data.slice(0, 10).map((item, index) => {
          const primaryColor = getColor(index);
          const lighterColor = getLighterColor(primaryColor);
          const mediumColor = getMediumColor(primaryColor);
          const percentage = Math.round(((item.score + 1) / 10) * 100);
          return (
            <div 
              key={item.learning_objective} 
              className={`flex items-center justify-between w-full p-1 rounded-full ${lighterColor} hover:shadow-md transition-shadow duration-300`}
            >
              <div className="relative group w-1/5">
                <div className={`text-left text-sm p-1 rounded-full ${primaryColor} text-white text-center hover:opacity-90 transition-opacity duration-300`}>
                  {item.learning_objective.slice(-3)}
                </div>
                <div className={`absolute hidden group-hover:block ${primaryColor} text-white text-xs rounded-lg p-2 w-48 z-10 left-full ml-2`}>
                  {item.descriptions}
                </div>
              </div>
              <div className="relative w-3/4 h-2 mx-2 rounded-full bg-gray-200 hover:shadow-inner transition-shadow duration-300">
                <div className={`absolute inset-0 ${mediumColor} rounded-full overflow-hidden`}>
                  <div
                    className={`absolute left-0 h-full transition-all duration-300 ${primaryColor} rounded-full`}
                    style={{ width: `${percentage}%` }}
                  ></div>
                </div>
              </div>
              <div className="text-sm w-16 font-medium text-center">{percentage.toFixed(0)}</div>
            </div>
          );
        })}
      </div>
    </div>
  );
};

export default LearningObjectiveChart;
