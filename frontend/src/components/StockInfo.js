import React from 'react'
import { Grid, List, ListItem, Box } from "@mui/material";
import { LineChart } from '@mui/x-charts/LineChart';
import dayjs from "dayjs";
import { FaCheckSquare } from "react-icons/fa";

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
const companyClosePrice = [68600, 69700, 69600, 69600, 69600, 70900, 70900, 69900, 70300, 70500, 70500, 70500, 70400, 70800, 72200, 72800, 72500, 72500, 72500, 72700]
const stockDateList = ["2023-11-01",
  "2023-11-02",
  "2023-11-03",
  "2023-11-04",
  "2023-11-05",
  "2023-11-06",
  "2023-11-07",
  "2023-11-08",
  "2023-11-09",
  "2023-11-10",
  "2023-11-11",
  "2023-11-12",
  "2023-11-13",
  "2023-11-14",
  "2023-11-15",
  "2023-11-16",
  "2023-11-17",
  "2023-11-18",
  "2023-11-19",
  "2023-11-20"]
const stockDate = stockDateList.map((date) => new Date(date.split('-')))
const date = dayjs().format('YYYY.MM.DD')
export default function StockInfo(props) {
  return (
    <>
      <Grid container sx={{ display: "flex", flexDirection: "row" }}>
        <Grid sx={{ width: "72%" }}>
          <Box sx={{ bgcolor: "#b0e2e8", p: 0.3, pl: 1, fontFamily: "GmarketSansMedium", display: "flex", alignItems: "center" }}>
            <FaCheckSquare />&nbsp; {props.companyId ? companyNames[props.companyId - 48] : "삼성전자"} {date} 주가 현황
          </Box>
          <Box height={"38vh"}>
            <LineChart skipAnimation
              xAxis={[
                {
                  data: stockDate,
                  scaleType: 'time',
                  valueFormatter: (date) => dayjs(date).format("YY MMM DD"),
                  tickLabelStyle: {
                    fontSize: 10
                  }
                }
              ]}
              yAxis={[
                {
                  tickLabelStyle: {
                    fontSize: 10
                  }
                }
              ]}
              series={[
                {
                  curve: "linear",
                  showMark: false,
                  label: "Stock Close Price",
                  data: companyClosePrice,
                },
              ]}
              slotProps={{ legend: { hidden: true } }}
            />
          </Box>
        </Grid>
        <Grid width={"28%"} p={1} pt={0.5} bgcolor={"#eff7d9"} sx={{ display: "flex", alignItems: "center" }}>
          <List>
            <ListItem sx={{ p: 0.1, fontSize: "0.65rem", fontFamily: "Noto Sans KR" }}>
              <b>시가총액</b>&nbsp; | {props.companyInfo["시가총액"] ? props.companyInfo["시가총액"].toLocaleString() : props.companyInfo["시가총액"]}원
            </ListItem>
            <ListItem sx={{ p: 0.1, fontSize: "0.65rem", fontFamily: "Noto Sans KR" }}>
              <b>등락률</b>&nbsp; | {props.companyInfo["등락률"]}%
            </ListItem>
            <ListItem sx={{ p: 0.1, fontSize: "0.65rem", fontFamily: "Noto Sans KR" }}>
              <b>거래량</b>&nbsp; | {props.companyInfo["거래량"]}주
            </ListItem>
            <ListItem sx={{ p: 0.1, fontSize: "0.65rem", fontFamily: "Noto Sans KR" }}>
              <b>거래대금</b>&nbsp; | {props.companyInfo["거래대금"] ? props.companyInfo["거래대금"].toLocaleString() : props.companyInfo["거래대금"]}원
            </ListItem>
            <ListItem sx={{ p: 0.1, fontSize: "0.65rem", fontFamily: "Noto Sans KR" }}>
              <b>상장주식수</b>&nbsp; | {props.companyInfo["상장주식수"]}주
            </ListItem>
            <ListItem sx={{ p: 0.1, fontSize: "0.65rem", fontFamily: "Noto Sans KR" }}>
              <b>BPS</b>&nbsp; | {props.companyInfo["BPS"] ? props.companyInfo["BPS"].toLocaleString() : props.companyInfo["BPS"]}원
            </ListItem>
            <ListItem sx={{ p: 0.1, fontSize: "0.65rem", fontFamily: "Noto Sans KR" }}>
              <b>EPS</b>&nbsp; | {props.companyInfo["EPS"] ? props.companyInfo["EPS"].toLocaleString() : props.companyInfo["EPS"]}원
            </ListItem>
            <ListItem sx={{ p: 0.1, fontSize: "0.65rem", fontFamily: "Noto Sans KR" }}>
              <b>PER</b>&nbsp; | {props.companyInfo["PER"]}배
            </ListItem>
            <ListItem sx={{ p: 0.1, fontSize: "0.65rem", fontFamily: "Noto Sans KR" }}>
              <b>PBR</b>&nbsp; | {props.companyInfo["PBR"]}배
            </ListItem>
            <ListItem sx={{ p: 0.1, fontSize: "0.65rem", fontFamily: "Noto Sans KR" }}>
              <b>DPS</b>&nbsp; | {props.companyInfo["DPS"]}
            </ListItem>
            <ListItem sx={{ p: 0.1, fontSize: "0.65rem", fontFamily: "Noto Sans KR" }}>
              <b>외국인보유수량</b>&nbsp; | {props.companyInfo["외국인보유수량"]}주
            </ListItem>
            <ListItem sx={{ p: 0.1, fontSize: "0.65rem", fontFamily: "Noto Sans KR" }}>
              <b>외국인지분율</b>&nbsp; | {props.companyInfo["외국인지분율"]}%
            </ListItem>
            <ListItem sx={{ p: 0.1, fontSize: "0.65rem", fontFamily: "Noto Sans KR" }}>
              <b>외국인지분율</b>&nbsp; | {props.companyInfo["외국인지분율"]}%
            </ListItem>
            <ListItem sx={{ p: 0.1, fontSize: "0.65rem", fontFamily: "Noto Sans KR" }}>
              <b>외국인지분율</b>&nbsp; | {props.companyInfo["외국인지분율"]}%
            </ListItem>
            <ListItem sx={{ p: 0.1, fontSize: "0.65rem", fontFamily: "Noto Sans KR" }}>
              <b>외국인지분율</b>&nbsp; | {props.companyInfo["외국인지분율"]}%
            </ListItem>
            <ListItem sx={{ p: 0.1, fontSize: "0.65rem", fontFamily: "Noto Sans KR" }}>
              <b>외국인지분율</b>&nbsp; | {props.companyInfo["외국인지분율"]}%
            </ListItem>
          </List>
        </Grid>
      </Grid>
    </>
  )
}
