import React, { useState, useEffect } from 'react'
import {
  Box,
  Grid,
  Typography
} from '@mui/material'
import dayjs from "dayjs";
import ReportEconomyInfo from '../components/ReportEconomyInfo';
import ReportCompanyTopic from '../components/ReportCompanyTopic';
import '../css/font.css'
import { FaQuoteLeft, FaQuoteRight } from "react-icons/fa";
import axios from 'axios'

export default function Report(tabNum) {
  const date = dayjs().subtract(1, "day").format('YYYY년 MM월 DD일')
  const [companyTopic, setCompanyTopic] = useState([])
  const [economyInfo, setEconomyInfo] = useState([])
  useEffect(() => {
    const FetchReportContent = async () => {
      try {
        const response = await axios.get('http://localhost:8000/jh/get-last')
        setCompanyTopic(response.data)
      } catch (err) {
        console.log()
      }
    }
    const FetchEconomyInfo = async () => {
      try {
        const response = await axios.get('http://localhost:8000/jh/get-economy-info')
        console.log("economy: ", response.data)
        // setEconomyInfo(response.data)
      } catch (err) {
        console.log()
      }
    }
    FetchReportContent()
    FetchEconomyInfo()
  }, [tabNum])

  return (
    <>
      <Grid sx={{ display: "flex", justifyContent: "center" }}>
        <Box sx={{ width: "75vw", height: "86vh", mt: 4, border: "1px solid #b4b4b4", borderRadius: 4, display: "flex", justifySelf: "center", flexDirection: "column" }}>
          <Box sx={{ position: "absolute", top: "6.5rem", left: "30.5vw", bgcolor: "white", p: 1 }}><FaQuoteLeft /></Box>
          <Box sx={{ position: "absolute", top: "11rem", left: "67vw", bgcolor: "white", p: 1 }}><FaQuoteRight /></Box>
          <Box mt={5} alignSelf={"center"} p={2} pl={5} pr={5} border={"2px solid #68a29d"}>
            <Typography sx={{ fontSize: "1.5rem", fontFamily: "SebangGothic", fontWeight: "400" }}>
              {date}의 경제를 알려드립니다
            </Typography>
          </Box>
          <Box m={2} width={"55vw"} alignSelf={"center"} >
            <ReportEconomyInfo />
            <ReportCompanyTopic
              companyTopic={companyTopic} />
          </Box>
        </Box>
      </Grid>
    </>
  )
}
