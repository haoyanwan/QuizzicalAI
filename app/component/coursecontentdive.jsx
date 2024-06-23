import React, { useState, useEffect } from "react";

const CourseContentDive = () => {
  const [weakestPoint, setWeakestPoint] = useState(null);
  const [resources, setResources] = useState([]);

  useEffect(() => {
    const fetchWeakestKnowledgePoint = async () => {
      try {
        const response = await fetch("/api/weakest_knowledge_point");
        const data = await response.json();
        if (data) {
          setWeakestPoint(data);
          queryYouCom(data.knowledge);
        }
      } catch (error) {
        console.error("Error fetching weakest knowledge point:", error);
      }
    };

    const queryYouCom = async (knowledge) => {
      try {
        const response = await fetch("/api/query_you_com", {
          method: "POST",
          headers: {
            "Content-Type": "application/json"
          },
          body: JSON.stringify({ knowledge })
        });
        const result = await response.json();

        if (result.search_results) {
          const data = result.search_results.map((item) => ({
            url: item.url,
            name: item.name,
            snippet: item.snippet,
          }));
          setResources(data);
        }
      } catch (error) {
        console.error("Error querying You.com:", error);
      }
    };

    fetchWeakestKnowledgePoint();
  }, []);

  return (
    <div className="course-content-dive">
      <h2>Course Content Dive</h2>
      {weakestPoint ? (
        <div>
          <h3>Weakest Point: {weakestPoint.label}</h3>
          <p>{weakestPoint.knowledge}</p>
        </div>
      ) : (
        <p>Loading weakest knowledge point...</p>
      )}

      <h3>Recommended Resources</h3>
      <ul>
        {resources.map((resource, index) => (
          <li key={index}>
            <a href={resource.url} target="_blank" rel="noopener noreferrer">
              {resource.name}
            </a>
            <p>{resource.snippet}</p>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default CourseContentDive;
