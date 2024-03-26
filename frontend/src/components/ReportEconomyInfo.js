import React from 'react'
import {
  Grid,
  List,
  ListItem,
  Typography,
} from '@mui/material'
import { RiArrowUpSFill, RiArrowDownSFill } from "react-icons/ri";

const leftInfoList = [
  "코스피",
  "코스닥",
  "코스피200",
  "비트코인",
  "SnP500",
  "나스닥",
  "다우존스",
]
const leftInfoName = [
  "코스피",
  "코스닥",
  "코스피200",
  "비트코인($)",
  "S&P500",
  "NASDAQ",
  "Dow Jones"
]
const rightInfoList = [
  "환율_원화",
  "금",
  "WTI",
  "한국채권_5년물",
  "한국채권_10년물",
  "미국채권_5년물",
  "미국채권_10년물"
]
const rightInfoName = [
  "환율(달러)",
  "금(선물)",
  "WTI",
  "한국채권 5년물",
  "한국채권 10년물",
  "미국채권 5년물",
  "미국채권 10년물"
]

export default function ReportContents(props) {
  return (
    <>
      <Grid sx={{ display: "flex", justifyContent: "center" }}>
        <Grid sx={{ width: "40vw", height: "30vh", display: "flex", justifyContent: "space-evenly", alignItems: "center" }}>
          <Grid container sx={{ width: "20vw", display: "flex", flexDirection: "row", justifyContent: "space-between" }}>
            <List item sx={{ p: 0.5, display: "flex", flexDirection: "column" }}>
              {leftInfoList.map((info, idx) => (
                <ListItem container sx={{ p: 0, justifyContent: "left" }}>
                  <Typography sx={{ fontSize: "0.8rem", fontWeight: "bold" }}>{leftInfoName[idx]}</Typography>
                </ListItem>
              ))}
            </List>
            <List item sx={{ p: 0.5, display: "flex", flexDirection: "column" }}>
              {leftInfoList.map((info, idx) => (
                <ListItem container sx={{ p: 0, justifyContent: "center" }}>
                  <Typography sx={{ fontSize: "0.8rem" }}>
                    {props.economyInfo[info] ? props.economyInfo[info].toLocaleString() : props.economyInfo[info]}
                  </Typography>
                </ListItem>
              ))}
            </List>
            <List item sx={{ p: 0.5, display: "flex", flexDirection: "column" }}>
              {leftInfoList.map((info, idx) => (
                <ListItem container sx={{ p: 0, justifyContent: "right" }}>
                  <Typography sx={{ fontSize: "0.8rem", color: (props.economyUpdown[info + "_등락률"] < 0) ? "#ff5251" : (props.economyUpdown[info + "_등락률"] > 0) ? "#73d073" : "black" }}>
                    {props.economyUpdown[info + "_등락률"] ? props.economyUpdown[info + "_등락률"] + "%" : <span>—&nbsp;&nbsp;&nbsp;&nbsp;</span>}
                    {(props.economyUpdown[info + "_등락률"] > 0) && <RiArrowUpSFill color='#73d073' />}
                    {(props.economyUpdown[info + "_등락률"] < 0) && <RiArrowDownSFill color='#ff5251' />}
                  </Typography>
                </ListItem>
              ))}
            </List>
          </Grid>
          <Grid container sx={{ width: "20vw", display: "flex", flexDirection: "row", justifyContent: "space-between" }}>
            <List item sx={{ p: 0.5, display: "flex", flexDirection: "column" }}>
              {rightInfoList.map((info, idx) => (
                <ListItem container sx={{ p: 0, justifyContent: "left" }}>
                  <Typography sx={{ fontSize: "0.8rem", fontWeight: "bold" }}>{rightInfoName[idx]}</Typography>
                </ListItem>
              ))}
            </List>
            <List item sx={{ p: 0.5, display: "flex", flexDirection: "column" }}>
              {rightInfoList.map((info, idx) => (
                <ListItem container sx={{ p: 0, justifyContent: "center" }}>
                  <Typography sx={{ fontSize: "0.8rem" }}>
                    {(props.economyInfo[info] == "-100") ? <span>—&nbsp;&nbsp;&nbsp;&nbsp;</span> : props.economyInfo[info] ? props.economyInfo[info].toLocaleString() : props.economyInfo[info]}
                  </Typography>
                </ListItem>
              ))}
            </List>
            <List item sx={{ p: 0.5, display: "flex", flexDirection: "column" }}>
              {rightInfoList.map((info, idx) => (
                <ListItem container sx={{ p: 0, justifyContent: "right" }}>
                  <Typography sx={{ fontSize: "0.8rem", color: (props.economyUpdown[info + "_등락률"] < 0) && (props.economyInfo[info] != "-100") ? "#ff5251" : (props.economyUpdown[info + "_등락률"] > 0) && (props.economyInfo[info] != "-100") ? "#73d073" : "black" }}>
                    {(props.economyInfo[info] == "-100") ? <span>—&nbsp;&nbsp;&nbsp;&nbsp;</span> : props.economyUpdown[info + "_등락률"] ? props.economyUpdown[info + "_등락률"] + "%" : <span>—&nbsp;&nbsp;&nbsp;&nbsp;</span>}
                    {(props.economyUpdown[info + "_등락률"] > 0) && <RiArrowUpSFill color='#73d073' />}
                    {(props.economyUpdown[info + "_등락률"] < 0) && (props.economyInfo[info] != "-100") && <RiArrowDownSFill color='#ff5251' />}
                  </Typography>
                </ListItem>
              ))}
            </List>
          </Grid>
        </Grid>
      </Grid>
    </>
  )
}
