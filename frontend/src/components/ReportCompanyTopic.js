import React from 'react'
import {
  Grid,
  List,
  Typography,
  ListItem,
  Box,
  Divider,
} from '@mui/material'
// import { TbKeyframeFilled } from "react-icons/tb";
import { BsStickyFill } from "react-icons/bs";
import { RiBarChartBoxFill } from "react-icons/ri";
import { RiCornerDownRightFill } from "react-icons/ri";
import "../css/font.css";

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

export default function ReportCompanyTopic(props) {
  console.log(props.companyTopic)
  return (
    <>
      <Grid sx={{ display: "flex", justifyContent: "center" }}>
        <List>
          {props.companyTopic.map((company, idx) => (
            <Box sx={{ display: "flex", flexDirection: "column", pt: 1 }}>
              <Typography fontFamily={"SebangGothic"} fontSize={"1.2rem"} display={"flex"} alignItems={"center"}>
                <RiCornerDownRightFill color={idx % 2 == 1 ? "#6b6868" : "#82bab4"} fontSize={"1.5rem"} />&nbsp;&nbsp;{companyNames[idx]}
              </Typography>
              <Divider sx={{ borderColor: "#c1c1c1" }} />
              <List sx={{ pl: 4, pt: 0, listStyleType: "square" }}>
                <ListItem sx={{ display: "list-item", fontFamily: "Noto Sans KR", fontSize: "0.9rem" }}>
                  {company["topic_summary"]}
                </ListItem>
              </List>
            </Box>
          ))}
        </List>
      </Grid >
    </>
  )
}
