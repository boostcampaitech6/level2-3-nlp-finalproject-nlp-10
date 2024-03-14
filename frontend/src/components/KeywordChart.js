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
import { BubbleChart } from "react-bubble-chart";

export default function KeywordChart(props) {
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
          <List sx={{ p: 1, pl: 2.5, listStyleType: "square" }}>
            {props.topicTitleSummary.slice(0, 10).map((it, idx) => (
              <ListItem
                key={idx}
                sx={{
                  display: "list-item",
                  p: 0.5,
                  fontSize: "1rem",
                  fontFamily: "omyu_pretty",
                }}
              >
                {it}: {props.cnt[idx]}개
              </ListItem>
            ))}
          </List>
          {/* <BubbleChart
            graph={{
              zoom: 1.1,
              offsetX: -0.05,
              offsetY: -0.01,
            }}
            width={800}
            height={600}
            padding={0} // optional value, number that set the padding between bubbles
            showLegend // optional value, pass false to disable the legend.
            legendPercentage={20} // optional value, from 0 to 100.
            legendFont={{
              family: "Arial",
              size: 12,
              color: "#000",
              weight: "bold",
            }}
            valueFont={{
              family: "Arial",
              size: 12,
              color: "#fff",
              weight: "bold",
            }}
            labelFont={{
              family: "Arial",
              size: 16,
              color: "#fff",
              weight: "bold",
            }}
            data={data}
          /> */}
        </Box>
      </Box>
    </>
  );
}
