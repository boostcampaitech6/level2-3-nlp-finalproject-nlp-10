import React from 'react'
import {
  Box,
  Grid,
  Typography
} from '@mui/material'
import dayjs from "dayjs";
import '../css/font.css'
import { AiFillPushpin } from "react-icons/ai";

export default function Report() {
  const date = dayjs().subtract(1, "day").format('YYYY년 MM월 DD일')

  return (
    <>
      <Grid sx={{ height: "90vh", display: "flex", justifyContent: "center" }}>
        <Box sx={{ width: "75vw", height: "75vh", mt: 6, border: "20px solid #8fd0ca", borderRadius: 3, display: "flex", flexDirection: "column" }}>
          <Box mt={5} alignSelf={"center"}>
            <Typography sx={{ fontSize: "1.5rem", fontFamily: "GmarketSansMedium" }}>
              [ {date}의 경제를 알려드립니다 ]
            </Typography>
          </Box>
          <Box mt={2} width={"60vw"} alignSelf={"center"} border={"1px solid lightgray"}>

          </Box>
        </Box>
      </Grid>
    </>
  )
}
