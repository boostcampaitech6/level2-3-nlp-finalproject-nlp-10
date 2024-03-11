import React, { useState } from 'react'
import {
  Divider,
  Grid,
  Box,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
} from '@mui/material'

export default function FilterTab() {
  const [date, setDate] = useState("");

  const handleChangeDate = (event) => {
    setDate(event.target.value);
  };

  const [company, setCompany] = useState("");

  const handleChangeCompany = (event) => {
    setCompany(event.target.value);
  };
  return (
    <>

      <Box sx={{ display: "flex" }}>
        <Grid container >
          <Grid md={2} sm={3} xs={4} sx={{ p: 2 }}>
            <FormControl
              fullWidth
              sx={{ backgroundColor: "white" }}
            >
              <InputLabel id="demo-simple-select-label">
                Date
              </InputLabel>
              <Select
                labelId="demo-simple-select-label"
                id="demo-simple-select"
                value={date}
                label="Date"
                onChange={handleChangeDate}
                sx={{ height: "3rem", fontSize: "0.9rem", }}
              >
                <MenuItem value={10}>하루</MenuItem>
                <MenuItem value={20}>일주일</MenuItem>
                <MenuItem value={30}>한 달</MenuItem>
              </Select>
            </FormControl>
          </Grid>
          <Grid md={2} sm={3} xs={4} sx={{ p: 2 }}>
            <FormControl
              fullWidth
              sx={{ backgroundColor: "white" }}
            >
              <InputLabel id="demo-simple-select-label">
                Company
              </InputLabel>
              <Select
                labelId="demo-simple-select-label"
                id="demo-simple-select"
                value={company}
                label="Company"
                onChange={handleChangeCompany}
                sx={{ height: "3rem", fontSize: "0.9rem", }}
              >
                <MenuItem value={10}>삼성</MenuItem>
                <MenuItem value={20}>LG에너지솔루션</MenuItem>
                <MenuItem value={30}>SK 하이닉스</MenuItem>
              </Select>
            </FormControl>
          </Grid>
        </Grid>
      </Box>
      <Divider />
    </>
  )
}
