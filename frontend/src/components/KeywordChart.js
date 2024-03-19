import React from "react";
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
import diagram from "../img/diagram.png";
import { IconContext } from "react-icons";
import BubbleCrt from "./Bubble";
import Bu from "./Bu";
import Example from "./Example";

export default function KeywordChart({
  cnt,
  topicId,
  topicSummary,
  topicTitleSummary,
  title,
}) {
  const data = [
    { label: "Category 1", value: 20, color: "#ff0000" },
    { label: "Category 2", value: 30, color: "#00ff00" },
    { label: "Category 3", value: 40, color: "#0000ff" },
  ];
  return (
    <>
      <Box sx={{ display: "flex", mt: 3 }}>
        <IconContext.Provider value={{ size: "25px" }}>
          <VscSymbolKeyword />
        </IconContext.Provider>
        <Typography
          variant="h5"
          sx={{
            fontFamily: "KOTRAHOPE",
            fontWeight: "normal",
            pl: 1.3,
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
            padding: "10px",
          }}
        >
          {/* <Bu
            cnt={cnt}
            topicId={topicId}
            topicSummary={topicSummary}
            topicTitleSummary={topicTitleSummary}
            title={title}
          /> */}
          <Example
            cnt={cnt}
            topicId={topicId}
            topicSummary={topicSummary}
            topicTitleSummary={topicTitleSummary}
            title={title}
          />
        </Box>
      </Box>
    </>
  );
}
