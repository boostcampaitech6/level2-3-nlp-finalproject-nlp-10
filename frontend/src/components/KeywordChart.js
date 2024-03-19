import React from "react";
import { useState, useEffect, useRef } from "react";
import "../css/font.css";
import "../css/layout.css";
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
import { VscSymbolKeyword } from "react-icons/vsc";
import { IconContext } from "react-icons";
import BubbleCrt from "./Bubble";
import Bu from "./Bu";
import Bub from "./Bub";
import Example from "./Example";
import { FaBrain } from "react-icons/fa";
import { BubbleChart } from "react-bubble-chart";
import { TbArrowBadgeRightFilled } from "react-icons/tb";

export default function KeywordChart({
  cnt,
  topicId,
  topicSummary,
  topicTitleSummary,
  title,
  confirm,
}) {
  const data = [
    { label: "Category 1", value: 20, color: "#ff0000" },
    { label: "Category 2", value: 30, color: "#00ff00" },
    { label: "Category 3", value: 40, color: "#0000ff" },
  ];

  const [diagram, setDiagram] = useState([]);
  const [diagram2, setDiagram2] = useState([]);
  const colorHere = [
    "rgb(255, 69, 96)",
    "rgb(254, 176, 25)",
    "rgb(0, 143, 251)",
    "rgb(119, 93, 208)",
    "rgb(0, 227, 150)",
    "#FF9B7B",
    "#519F5B",
    "#CD7A4B",
    "#00A0D3",
    "#73676B",
  ];
  const sizeHere = [68, 51, 15, 11, 11, 6, 7, 7, 5, 5];
  useEffect(() => {
    const newDiagram = topicTitleSummary.slice(0, 8).map((title, index) => ({
      label:
        title.slice(0, title.length / 4) +
        "\n" +
        title.slice(title.length / 4, title.length / 2),
      label2: title,
      value: cnt[index],
      color: colorHere[index],
    }));
    setDiagram(newDiagram);
    console.log("diagram", diagram);
  }, [title]);
  return (
    <>
      <Box sx={{ display: "flex", mt: 3 }}>
        <IconContext.Provider value={{ size: "30px" }}>
          <TbArrowBadgeRightFilled color="#34b37d" />
        </IconContext.Provider>
        <Typography
          variant="h5"
          sx={{
            fontFamily: "GmarketSansMedium",
            fontWeight: "bold",
            pl: 1,
          }}
        >
          핵심 키워드
        </Typography>
      </Box>

      <Box sx={{ p: 1, pb: 3 }}>
        <Box
          sx={{
            minHeight: "10rem",
            // borderRadius: "20px",
            // border: "5px solid rgb(218, 248, 240)",
            border: "2px solid #54cc99",
            borderRadius: "25px",
            // padding: "10px",
          }}
        >
          {/* <Bu
            cnt={cnt}
            topicId={topicId}
            topicSummary={topicSummary}
            topicTitleSummary={topicTitleSummary}
            title={title}
            diagram={diagram}
          /> */}
          {/* <Example
            cnt={cnt}
            topicId={topicId}
            topicSummary={topicSummary}
            topicTitleSummary={topicTitleSummary}
            title={title}
            // diagram={diagram}
          /> */}
          <Bub diagram={diagram} confirm={confirm} />
        </Box>
      </Box>
    </>
  );
}
