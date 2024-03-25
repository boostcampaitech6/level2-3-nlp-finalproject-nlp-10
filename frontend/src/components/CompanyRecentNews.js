import React from "react";
import "../css/font.css";
import "../css/layout.css";
import { Box, Typography, List, ListItem } from "@mui/material";
import {
  BsEmojiSmileFill,
  BsEmojiFrownFill,
  BsFillEmojiSurpriseFill,
} from "react-icons/bs";

export default function CompanyRecentNews(props) {
  return (
    <>
      {props.newsId.slice(0, 30).map((news, idx) => (
        <Box
          key={idx}
          sx={{
            p: 2,
            mb: 2,
            border: "1px solid lightgray",
            borderRadius: "10px",
          }}
        >
          <Typography variant="h7" sx={{ p: 1, fontWeight: "bold", fontFamily: "Noto Sans KR" }}>
            "{props.newsTitle[idx]}"
          </Typography>

          <Typography sx={{ pl: 2, fontFamily: "Noto Sans KR" }}>
            {props.summary[idx]}
          </Typography>
          <Box
            sx={{ pl: 1, pt: 1, fontSize: "0.8rem", color: "gray", fontFamily: "Noto Sans KR", display: "flex", alignItems: "center" }}
          >
            {props.sentiment[idx] == 2 && <BsEmojiSmileFill color="#5dc2b1" />}
            {props.sentiment[idx] == 1 && <BsFillEmojiSurpriseFill color="#f0d689" />}
            {props.sentiment[idx] == 0 && <BsEmojiFrownFill color="#ed9568" />}
            &nbsp;| 관련 뉴스 {props.cnt}건
          </Box>
        </Box>
      ))}
    </>
  );
}
