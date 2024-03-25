import React from 'react'
import { PieChart, pieArcLabelClasses } from '@mui/x-charts/PieChart';
import { Box, Grid, Divider, List, ListItem, } from '@mui/material';
import dayjs from "dayjs";
import { FaCheckSquare } from "react-icons/fa";
import {
  BsEmojiSmileFill,
  BsEmojiFrownFill,
  BsFillEmojiSurpriseFill,
} from "react-icons/bs";

import "../css/font.css";


const date = dayjs().format('YYYY.MM.DD')

const data = [
  { label: '긍정', value: 25, color: '#5dc2b1' },
  { label: '중립', value: 30, color: '#f0d689' },
  { label: '부정', value: 17, color: '#ed9568' },
];

const getArcLabel = (params) => {
  return `${params.value}건`;
};

const companyNames = [
  "삼성",
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
  return (
    <>
      <Box sx={{ bgcolor: "#b0e2e8", p: 0.3, pl: 1, fontFamily: "GmarketSansMedium", display: "flex", alignItems: "center" }}>
        <FaCheckSquare /> &nbsp; {props.companyId ? companyNames[props.companyId - 48] : "삼성"} {date} 뉴스 체크
      </Box>
      <Grid container sx={{ display: "flex", flexDirection: "row", alignItems: "center" }}>
        <Grid sx={{ width: "40%" }}>
          <PieChart skipAnimation
            series={[
              {
                startAngle: -30,
                innerRadius: 40,
                outerRadius: 80,
                paddingAngle: 1,
                cornerRadius: 3,
                data,
                cx: 125,
                cy: 110,
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
            height={225}
            slotProps={{
              legend: { hidden: true },
            }}
          />
        </Grid>
        <Grid sx={{ width: "60%", display: "flex", flexDirection: "column", p: 0.5 }}>
          <Grid sx={{ display: "flex", flexDirection: "row", alignItems: "center" }}>
            <Grid sx={{ pl: 1, pr: 2, pt: 1 }}>
              <BsEmojiSmileFill color="#5dc2b1" fontSize={"3rem"} />
            </Grid>
            <List sx={{ pl: 2.5, listStyleType: "square" }}>
              <ListItem sx={{ display: "list-item", p: 0.5, fontFamily: "Noto Sans KR" }}>
                긍정 토픽1
              </ListItem>
              <ListItem sx={{ display: "list-item", p: 0.5, fontFamily: "Noto Sans KR" }}>
                긍정 토픽2
              </ListItem>
            </List>
          </Grid>
          <Divider />
          <Grid sx={{ display: "flex", flexDirection: "row", alignItems: "center" }}>
            <Grid sx={{ pl: 1, pr: 2, pt: 1 }}>
              <BsFillEmojiSurpriseFill color="#f0d689" fontSize={"3rem"} />
            </Grid>
            <List sx={{ pl: 2.5, listStyleType: "square" }}>
              <ListItem sx={{ display: "list-item", p: 0.5, fontFamily: "Noto Sans KR" }}>
                중립 토픽1
              </ListItem>
              <ListItem sx={{ display: "list-item", p: 0.5, fontFamily: "Noto Sans KR" }}>
                중립 토픽2
              </ListItem>
            </List>
          </Grid>
          <Divider />
          <Grid sx={{ display: "flex", flexDirection: "row", alignItems: "center" }}>
            <Grid sx={{ pl: 1, pr: 2, pt: 1 }}>
              <BsEmojiFrownFill color="#ed9568" fontSize={"3rem"} />
            </Grid>
            <List sx={{ pl: 2.5, listStyleType: "square" }}>
              <ListItem sx={{ display: "list-item", p: 0.5, fontFamily: "Noto Sans KR" }}>
                부정 토픽1
              </ListItem>
              <ListItem sx={{ display: "list-item", p: 0.5, fontFamily: "Noto Sans KR" }}>
                부정 토픽2
              </ListItem>
            </List>
          </Grid>
        </Grid>
      </Grid>
    </>
  )
}
