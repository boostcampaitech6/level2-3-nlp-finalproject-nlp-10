import React from "react";
import { useState, useEffect } from "react";
import { PieChart, Pie, Legend, Tooltip } from "recharts";
import {
  Box,
  createTheme,
  Grid,
  Container,
  Typography,
  Paper,
  InputLabel,
  MenuItem,
  FormControl,
  Select,
  Button,
  ButtonGroup,
  Divider,
  List,
  ListItem,
} from "@mui/material";

const data01 = [
  { name: "Group A", value: 400 },
  { name: "Group B", value: 300 },
  { name: "Group C", value: 300 },
  { name: "Group D", value: 200 },
  { name: "Group E", value: 278 },
  { name: "Group F", value: 189 },
];

export default function Bu({
  cnt,
  topicId,
  topicSummary,
  topicTitleSummary,
  title,
}) {
  const data01 = [
    { name: "Group A", value: 400 },
    { name: "Group B", value: 300 },
    { name: "Group C", value: 300 },
    { name: "Group D", value: 200 },
    { name: "Group E", value: 278 },
    { name: "Group F", value: 189 },
  ];

  const [diagram, setDiagram] = useState([]);

  useEffect(() => {
    const newDiagram = topicTitleSummary.slice(0, 5).map((title, index) => ({
      name: title,
      value: cnt[index],
      fill:
        index === 0
          ? "#D37676"
          : index === 1
          ? "#F1C27B"
          : index === 2
          ? "#FFD89C"
          : index === 3
          ? "#FFFF00"
          : index === 4
          ? "#A2CDB0"
          : "#85A389",
    }));
    setDiagram(newDiagram);
  }, [title]);

  return (
    <Box sx={{ display: "flex" }}>
      <Box>
        <PieChart width={300} height={300}>
          <Pie
            dataKey="value"
            isAnimationActive={false}
            data={diagram}
            cx={120}
            cy={150}
            outerRadius={80}
            // fill="#8884d8"
            label
          />
          <Tooltip />
        </PieChart>
      </Box>

      <List sx={{ pt: 8, listStyleType: "square" }}>
        {topicTitleSummary.slice(0, 5).map((it, idx) => (
          <ListItem
            key={idx}
            sx={{
              display: "list-item",
              p: 0.5,
              fontSize: "1rem",
              fontFamily: "omyu_pretty",
              color:
                idx === 0
                  ? "#D37676"
                  : idx === 1
                  ? "#F1C27B"
                  : idx === 2
                  ? "#FFD89C"
                  : idx === 3
                  ? "#FFFF00"
                  : idx === 4
                  ? "#A2CDB0"
                  : "#85A389",
            }}
          >
            {it}
          </ListItem>
        ))}
      </List>
    </Box>
  );
}
