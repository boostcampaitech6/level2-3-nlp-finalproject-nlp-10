import React, { useEffect } from 'react'
import { Grid, List, ListItem, Box } from "@mui/material";
// import { LineChart } from '@mui/x-charts/LineChart';
import { LineChart, Line, CartesianGrid, XAxis, YAxis, Tooltip, Label } from 'recharts';
import dayjs from "dayjs";
import { FaCheckSquare } from "react-icons/fa";
import "../css/font.css"

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

const date = dayjs().format('YYYY.MM.DD')
export default function StockInfo(props) {
  // console.log("dict: ", props.closePriceInfo[1].map((price, idx) => { return { "date": new Date(props.closePriceInfo[0][idx].split('-')), "price": price } }))
  // const closePriceList = props.closePriceInfo[1] ? props.closePriceInfo[1].map((price, idx) => price) : []
  const data = props.closePriceInfo[1] ? props.closePriceInfo[1].map((price, idx) => { return { "date": new Date(props.closePriceInfo[0][idx].split('-')), "price": price } }).reverse() : []
  return (
    <>
      <Grid container sx={{ display: "flex", flexDirection: "row" }}>
        <Grid sx={{ width: "72%" }}>
          <Box sx={{ bgcolor: "#b0e2e8", p: 0.3, pl: 1, fontFamily: "GmarketSansMedium", display: "flex", alignItems: "center" }}>
            <FaCheckSquare />&nbsp; {props.companyId ? companyNames[props.companyId - 48] : "삼성전자"} {date} 주가 현황
          </Box>
          <Box height={"38vh"}>
            <LineChart width={440} height={270} data={data} margin={{ top: 35, right: 20 }}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="date" scale={"time"} interval={10} angle={10}
                style={{
                  fontSize: '0.7rem',
                }}
                tickFormatter={(label) => dayjs(label).format("YYMMMDD")} />
              <YAxis type="number" domain={['auto', 'auto']}
                style={{
                  fontSize: '0.7rem',
                }}
                tickFormatter={(price) => price.toLocaleString()}>
                <Label value="(원)" position="top" offset={10} style={{ fontSize: "0.7rem" }} />
              </YAxis>
              <Tooltip
                separator=' | '
                itemStyle={{ color: "black", fontSize: "0.9rem", fontWeight: "bold", fontFamily: "Noto Sans KR" }}
                formatter={(price) => price.toLocaleString() + "원"}
                labelStyle={{ fontSize: "0.8rem", fontFamily: "Noto Sans KR" }}
                labelFormatter={(label) => dayjs(label).format("YYYY MMM DD")}
              />
              <Line type="linear" dataKey="price" stroke="#1CB0A3" strokeWidth={2} dot={false} />
            </LineChart>
            {/* <LineChart skipAnimation
              xAxis={[
                {
                  data: props.closePriceInfo[0] ? props.closePriceInfo[0].map((date) => new Date(date.split('-'))) : [],
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
                  data: closePriceList,
                  valueFormatter: (price) => price.toString() + "₩"
                },
              ]}
              tooltip={{ trigger: 'axis' }}
              axisHighlight={{
                x: 'none', // Or 'none', or 'band'
                y: 'line', // Or 'none'
              }}
              slotProps={{ legend: { hidden: true } }}
            /> */}
          </Box>
        </Grid>
        <Grid width={"28%"} pl={1} pt={0.5} bgcolor={"#eff7d9"} sx={{ display: "flex", alignItems: "center" }}>
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
              <b>시가</b>&nbsp; | {props.companyInfo["시가"]}원
            </ListItem>
            <ListItem sx={{ p: 0.1, fontSize: "0.65rem", fontFamily: "Noto Sans KR" }}>
              <b>종가</b>&nbsp; | {props.companyInfo["종가"]}원
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
              <b>DIV</b>&nbsp; | {props.companyInfo["DIV"]}%
            </ListItem>
            <ListItem sx={{ p: 0.1, fontSize: "0.65rem", fontFamily: "Noto Sans KR" }}>
              <b>DPS</b>&nbsp; | {props.companyInfo["DPS"]}%
            </ListItem>
            <ListItem sx={{ p: 0.1, fontSize: "0.65rem", fontFamily: "Noto Sans KR" }}>
              <b>외국인보유수량</b>&nbsp; | {props.companyInfo["외국인보유수량"]}주
            </ListItem>
            <ListItem sx={{ p: 0.1, fontSize: "0.65rem", fontFamily: "Noto Sans KR" }}>
              <b>외국인지분율</b>&nbsp; | {props.companyInfo["외국인지분율"]}%
            </ListItem>
            <ListItem sx={{ p: 0.1, fontSize: "0.65rem", fontFamily: "Noto Sans KR" }}>
              <b>외국인한도수량</b>&nbsp; | {props.companyInfo["외국인한도수량"]}주
            </ListItem>
            <ListItem sx={{ p: 0.1, fontSize: "0.65rem", fontFamily: "Noto Sans KR" }}>
              <b>외국인한도소진률</b>&nbsp; | {props.companyInfo["외국인한도소진률"]}%
            </ListItem>
          </List>
        </Grid>
      </Grid>
    </>
  )
}
