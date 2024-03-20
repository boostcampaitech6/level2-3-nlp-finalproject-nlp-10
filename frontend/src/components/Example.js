import React from "react";
import { Treemap, Tooltip } from "recharts";
import { useState, useEffect, useRef } from "react";
import { Box, Typography, List, ListItem } from "@mui/material";

const data = [
  {
    name: "axis",
    size: 64,
  },
  {
    name: "controls",
    size: 32,
  },
  {
    name: "data",
    size: 8,
  },
  {
    name: "events",
    size: 8,
  },
  {
    name: "legend",
    size: 4,
  },
  {
    name: "operator",
    size: 4,
  },
];

const COLORS = [
  "#8889DD",
  "#9597E4",
  "#8DC77B",
  "#A5D297",
  "#E2CF45",
  "#F8C12D",
];

const CustomizedContent = (props) => {
  const {
    root,
    depth,
    x,
    y,
    width,
    height,
    index,
    colors,
    name,
    value,
    diagram,
    size,
  } = props;

  return (
    <g>
      <rect
        x={x}
        y={y}
        width={width}
        height={height}
        style={{
          fill:
            depth < 2
              ? colors[Math.floor((index / root.children.length) * 6)]
              : "none",
          stroke: "#fff",
          strokeWidth: 2 / (depth + 1e-10),
          strokeOpacity: 1 / (depth + 1e-10),
        }}
      />
      {depth === 1 ? (
        <text
          x={x + width / 2}
          y={y + height / 2 + 7}
          textAnchor="middle"
          fill="#fff"
          fontSize={14}
        >
          {name}
        </text>
      ) : null}
      {depth === 1 ? (
        <text x={x + 4} y={y + 18} fill="#fff" fontSize={8} fillOpacity={0.9}>
          {index + 1}
        </text>
      ) : null}
    </g>
  );
};

export default function Example({
  cnt,
  topicId,
  topicSummary,
  topicTitleSummary,
  title,
}) {
  const [diagram, setDiagram] = useState([]);
  useEffect(() => {
    const newDiagram = topicTitleSummary.slice(0, 6).map((title, index) => ({
      name: title,
      size: cnt[index],
    }));
    setDiagram(newDiagram);
    console.log("diagram", diagram);
  }, [title]);

  return (
    <Box sx={{ border: "1px solid black" }}>
      <Treemap
        width={400}
        height={200}
        data={diagram}
        dataKey="size"
        stroke="#fff"
        fill="#8884d8"
        content={<CustomizedContent colors={COLORS} />}
      >
        <Tooltip />
      </Treemap>
    </Box>
  );
}
