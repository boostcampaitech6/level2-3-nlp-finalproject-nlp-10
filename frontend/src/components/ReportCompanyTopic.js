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
  '삼성전자',
  'SK하이닉스',
  'LG에너지솔루션',
  '삼성바이오로직스',
  '기아',
  '현대차',
  '셀트리온',
  'POSCO홀딩스',
  'NAVER',
  'LG화학',
  '삼성물산',
  '삼성SDI',
  'KB금융',
  '카카오',
  '신한지주',
  '현대모비스',
  '포스코퓨처엠',
  '하나금융지주',
  'LG전자',
  '삼성생명',
  '메리츠금융지주',
  'LG',
  'SK',
  '삼성화재',
  '카카오뱅크',
  'HMM',
  '한국전력',
  'SK이노베이션',
  'KT&G',
  '삼성에스디에스',
  '에코프로머티',
  '우리금융지주',
  'SK텔레콤',
  '크래프톤',
  '기업은행',
  '삼성전기',
  '두산에너빌리티',
  'HD현대중공업',
  '고려아연',
  'KT',
  '포스코인터내셔널',
  '하이브',
  '대한항공',
  'HD한국조선해양',
  'SK스퀘어',
  'S-Oil',
  '한화에어로스페이스'
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
