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
} from "@mui/material";
import { VscSymbolKeyword } from "react-icons/vsc";
import diagram from "../img/diagram.png";
import { IconContext } from "react-icons";

export default function KeywordChart() {
  return (
    <>

      <Box sx={{ display: "flex", mt: 3, }}>
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
          오늘의 키워드
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
          <Box
            component="img"
            src={diagram}
            sx={{
              objectFit: "contain",
              width: "100%",
              height: "100%",
            }}
          />
        </Box>
      </Box>
    </>
  )
}
