import React, { useState } from "react";
import {
  Divider,
  Grid,
  Box,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Button,
} from "@mui/material";

export default function FilterTab({
  changeStartDate,
  changeEndDate,
  changeCompany,
  changeConfirm,
}) {
  const [startDate, setStartDate] = useState("");
  const [endDate, setEndDate] = useState("");

  const handleChangeStartDate = (event) => {
    changeStartDate(event.target.value);
    setStartDate(event.target.value);
    console.log("startDate", event.target.value);
  };

  const handleChangeEndDate = (event) => {
    changeEndDate(event.target.value);
    setEndDate(event.target.value);
    console.log("endDate", event.target.value);
  };

  const [company, setCompany] = useState("");

  const handleChangeCompany = (event) => {
    changeCompany(event.target.value);
    setCompany(event.target.value);
    console.log("company", event.target.value);
  };

  const [confirm, setConfirm] = useState(true);
  const handleChangeConfirm = (event) => {
    changeConfirm(!confirm);
    setConfirm(!confirm);
    console.log("confirm", confirm);
  };

  return (
    <>
      <Box sx={{ display: "flex" }}>
        <Grid container>
          <Grid md={2} sm={3} xs={4} sx={{ p: 2 }}>
            <FormControl fullWidth sx={{ backgroundColor: "white" }}>
              <InputLabel id="demo-simple-select-label">Start Date</InputLabel>
              <Select
                labelId="demo-simple-select-label"
                id="demo-simple-select"
                value={startDate}
                label="startDate"
                onChange={handleChangeStartDate}
                sx={{ height: "3rem", fontSize: "0.9rem" }}
              >
                <MenuItem value={"2023-11-01"}>2023-11-01</MenuItem>
                <MenuItem value={"2023-11-02"}>2023-11-02</MenuItem>
                <MenuItem value={"2023-11-03"}>2023-11-03</MenuItem>
                <MenuItem value={"2023-11-04"}>2023-11-04</MenuItem>
                <MenuItem value={"2023-11-05"}>2023-11-05</MenuItem>
                <MenuItem value={"2023-11-06"}>2023-11-06</MenuItem>
                <MenuItem value={"2023-11-07"}>2023-11-07</MenuItem>
                <MenuItem value={"2023-11-08"}>2023-11-08</MenuItem>
                <MenuItem value={"2023-11-09"}>2023-11-09</MenuItem>
                <MenuItem value={"2023-11-10"}>2023-11-10</MenuItem>
              </Select>
            </FormControl>
          </Grid>
          <Grid md={2} sm={3} xs={4} sx={{ p: 2 }}>
            <FormControl fullWidth sx={{ backgroundColor: "white" }}>
              <InputLabel id="demo-simple-select-label">End Date</InputLabel>
              <Select
                labelId="demo-simple-select-label"
                id="demo-simple-select"
                value={endDate}
                label="endDate"
                onChange={handleChangeEndDate}
                sx={{ height: "3rem", fontSize: "0.9rem" }}
              >
                <MenuItem value={"2023-11-01"}>2023-11-01</MenuItem>
                <MenuItem value={"2023-11-02"}>2023-11-02</MenuItem>
                <MenuItem value={"2023-11-03"}>2023-11-03</MenuItem>
                <MenuItem value={"2023-11-04"}>2023-11-04</MenuItem>
                <MenuItem value={"2023-11-05"}>2023-11-05</MenuItem>
                <MenuItem value={"2023-11-06"}>2023-11-06</MenuItem>
                <MenuItem value={"2023-11-07"}>2023-11-07</MenuItem>
                <MenuItem value={"2023-11-08"}>2023-11-08</MenuItem>
                <MenuItem value={"2023-11-09"}>2023-11-09</MenuItem>
                <MenuItem value={"2023-11-10"}>2023-11-10</MenuItem>
              </Select>
            </FormControl>
          </Grid>

          <Grid md={2} sm={3} xs={4} sx={{ p: 2 }}>
            <FormControl fullWidth sx={{ backgroundColor: "white" }}>
              <InputLabel id="demo-simple-select-label">Company</InputLabel>
              <Select
                labelId="demo-simple-select-label"
                id="demo-simple-select"
                value={company}
                label="Company"
                onChange={handleChangeCompany}
                sx={{ height: "3rem", fontSize: "0.9rem" }}
              >
                <MenuItem value={1}>삼성</MenuItem>
                <MenuItem value={2}>SK하이닉스</MenuItem>
                <MenuItem value={3}>LG에너지솔루션</MenuItem>
                <MenuItem value={4}>기아</MenuItem>
                <MenuItem value={5}>현대자동차</MenuItem>
                <MenuItem value={6}>셀트리온</MenuItem>
                <MenuItem value={7}>POSCO홀딩스</MenuItem>
                <MenuItem value={8}>Naver</MenuItem>
                <MenuItem value={9}>LG화학</MenuItem>
                <MenuItem value={10}>삼성물산</MenuItem>
                <MenuItem value={11}>삼성SDI</MenuItem>
                <MenuItem value={12}>KB금융</MenuItem>
                <MenuItem value={13}>카카오</MenuItem>
                <MenuItem value={14}>신한지주</MenuItem>
                <MenuItem value={15}>현대모비스</MenuItem>
                <MenuItem value={16}>포스코퓨처엠</MenuItem>
                <MenuItem value={17}>하나금융지주</MenuItem>
                <MenuItem value={18}>LG전자</MenuItem>
              </Select>
            </FormControl>
          </Grid>
          <Grid md={2} sm={3} xs={4} sx={{ p: 2.7 }}>
            <Button variant="outlined" onClick={handleChangeConfirm}>
              조회
            </Button>
          </Grid>
        </Grid>
      </Box>
      <Divider />
    </>
  );
}
