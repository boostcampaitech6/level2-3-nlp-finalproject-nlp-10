import React from "react";
import { PieChart, pieArcLabelClasses } from "@mui/x-charts/PieChart";
import { Box, Grid, Divider, List, ListItem } from "@mui/material";
import dayjs from "dayjs";
import { FaCheckSquare } from "react-icons/fa";
import {
  BsEmojiSmileFill,
  BsEmojiFrownFill,
  BsFillEmojiSurpriseFill,
} from "react-icons/bs";

import "../css/font.css";

const date = dayjs().format("YYYY.MM.DD");

const getArcLabel = (params) => {
  return `${params.value}건`;
};

const companyNames = [
  "삼성전자",
  "SK하이닉스",
  "LG에너지솔루션",
  "기아",
  "현대자동차",
  "셀트리온",
  "POSCO홀딩스",
  "Naver",
  "LG화학",
  "삼성물산",
  "삼성SDI",
  "KB금융",
  "카카오",
  "신한지주",
  "현대모비스",
  "포스코퓨처엠",
  "하나금융지주",
  "LG전자",
];

export default function SentimentInfo(props) {
  var data = [
    { label: "긍정", value: props.positiveNum, color: "#5dc2b1" },
    { label: "중립", value: props.neutralNum, color: "#f0d689" },
    { label: "부정", value: props.negativeNum, color: "#ed9568" },
  ];

  return (
    <>
      <Box
        sx={{
          bgcolor: "#b0e2e8",
          p: 0.3,
          pl: 1,
          fontFamily: "GmarketSansMedium",
          display: "flex",
          alignItems: "center",
        }}
      >
        <FaCheckSquare /> &nbsp;{" "}
        {props.companyId ? companyNames[props.companyId - 48] : "삼성전자"}{" "}
        {date} 인식 체크
      </Box>
      <Grid
        container
        sx={{ display: "flex", flexDirection: "row", alignItems: "center" }}
      >
        <Grid sx={{ width: "32%", height: "38vh" }}>
          <PieChart
            series={[
              {
                startAngle: -30,
                innerRadius: 40,
                outerRadius: 80,
                paddingAngle: 1,
                cornerRadius: 3,
                data,
                cx: 100,
                cy: 130,
                arcLabel: getArcLabel,
              },
            ]}
            sx={{
              [`& .${pieArcLabelClasses.root}`]: {
                // fill: 'white',
                fontSize: 12,
                fontWeight: "bold",
              },
            }}
            slotProps={{
              legend: { hidden: true },
            }}
          />
        </Grid>
        <Grid
          sx={{
            width: "68%",
            display: "flex",
            flexDirection: "column",
            p: 1,
          }}
        >
          <Grid
            sx={{ display: "flex", flexDirection: "row", alignItems: "center" }}
          >
            <Grid sx={{ pl: 1, pr: 2, pt: 1 }}>
              <BsEmojiSmileFill color="#5dc2b1" fontSize={"2.5rem"} />
            </Grid>
            <List sx={{ pl: 2.5, listStyleType: "square" }}>
              {props.sentimentNews[2].slice(0, 2).map((news, idx) => (
                <ListItem
                  sx={{
                    display: "list-item",
                    p: 0,
                    fontFamily: "Noto Sans KR",
                    fontSize: "0.9rem"
                  }}
                >
                  {news}
                </ListItem>
              ))}
            </List>
          </Grid>
          <Divider />
          <Grid
            sx={{ display: "flex", flexDirection: "row", alignItems: "center" }}
          >
            <Grid sx={{ pl: 1, pr: 2, pt: 1 }}>
              <BsFillEmojiSurpriseFill color="#f0d689" fontSize={"2.5rem"} />
            </Grid>
            <List sx={{ pl: 2.5, listStyleType: "square" }}>
              {props.sentimentNews[1].slice(0, 2).map((news, idx) => (
                <ListItem
                  sx={{
                    display: "list-item",
                    p: 0,
                    fontFamily: "Noto Sans KR",
                    fontSize: "0.9rem"
                  }}
                >
                  {news}
                </ListItem>
              ))}
            </List>
          </Grid>
          <Divider />
          <Grid
            sx={{ display: "flex", flexDirection: "row", alignItems: "center" }}
          >
            <Grid sx={{ pl: 1, pr: 2, pt: 0.5 }}>
              <BsEmojiFrownFill color="#ed9568" fontSize={"2.5rem"} />
            </Grid>
            <List sx={{ pl: 2.5, listStyleType: "square" }}>
              {props.sentimentNews[0].slice(0, 2).map((news, idx) => (
                <ListItem
                  sx={{
                    display: "list-item",
                    p: 0,
                    fontFamily: "Noto Sans KR",
                    fontSize: "0.9rem"
                  }}
                >
                  {news}
                </ListItem>
              ))}
            </List>
          </Grid>
        </Grid>
      </Grid>
    </>
  );
}
