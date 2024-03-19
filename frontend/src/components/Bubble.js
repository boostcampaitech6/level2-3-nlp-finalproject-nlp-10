import React from "react";
import { useState, useEffect } from "react";
import BubbleChart from "react-tooltip-bubble-chart";

export default function BubbleCrt({
  cnt,
  topicId,
  topicSummary,
  topicTitleSummary,
  title,
}) {
  const [diagram, setDiagram] = useState([]);

  useEffect(() => {
    const newDiagram = topicTitleSummary.slice(0, 5).map((title, index) => ({
      name: title.slice(0, 10),
      // value: cnt[index],
      size: 150,
      fillColor: "rgb(52, 202, 173, 0.3)",
      id: index,
      dYdX1: { dy: -2 + index, dx: -3 + index },
      dYdX2: { dy: 8 + index, dx: -20 + index },
    }));
    setDiagram(newDiagram);
  }, [title]);

  const bubbleData = [
    {
      fillColor: "rgb(52, 202, 173, 0.3)",
      id: 1,
      name: "Getting\nStart",
      size: 150,
      dYdX1: { dy: -2, dx: -3 },
      dYdX2: { dy: 8, dx: -20 },
    },
    {
      fillColor: "rgb(52, 202, 173, 0.3)",
      id: 2,
      name: "Getting\nStart",
      size: 120,
      dYdX1: { dy: -2, dx: -4 },
    },
    {
      fillColor: "rgb(52, 202, 173, 0.3)",
      id: 3,
      name: "Setting\nme",
      size: 90,
      dYdX1: { dy: -2, dx: -3 },
      dYdX2: { dy: 8, dx: -20 },
    },
    {
      fillColor: "rgb(52, 202, 173, 0.3)",
      id: 4,
      name: "Setting\nme2",
      size: 70,
      dYdX1: { dy: -2, dx: -4 },
    },
    {
      fillColor: "rgb(52, 202, 173, 0.3)",
      id: 5,
      name: "Setting\nme3",
      size: 50,
      dYdX1: { dy: 2, dx: 4 },
    },
  ];

  return (
    <div>
      {console.log("bubble ", topicTitleSummary)}
      <BubbleChart
        bubblesData={diagram}
        width={700}
        height={470}
        textFillColor="#717C84"
        backgroundColor="white"
        minValue={1}
        maxValue={150}
        move={true}
      />
    </div>
  );
}
