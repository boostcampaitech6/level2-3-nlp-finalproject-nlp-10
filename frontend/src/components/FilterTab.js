import React, { useState, useEffect } from "react";
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
import dayjs, { Dayjs } from "dayjs";
import { DemoContainer } from "@mui/x-date-pickers/internals/demo";
import { LocalizationProvider } from "@mui/x-date-pickers/LocalizationProvider";
import { AdapterDayjs } from "@mui/x-date-pickers/AdapterDayjs";
import { DatePicker } from "@mui/x-date-pickers/DatePicker";

export default function FilterTab({
  changeStartDate,
  changeEndDate,
  changeCompany,
  changeConfirm,
  tabNum,
}) {
  const today = new Date();
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

  // const [startDate, setStartDate] = useState(dayjs(`${today.getFullYear()}-${today.getMonth() + 1}-${today.getDate()}`));
  const [startDate, setStartDate] = useState("");
  const [endDate, setEndDate] = useState("");

  const handleChangeStartDate = (value) => {
    const formattedDate = dayjs(value).format("YYYY-MM-DD");
    console.log("startDate", formattedDate);
    console.log("startDate", typeof formattedDate);
    changeStartDate(formattedDate);
    setStartDate(formattedDate);
  };

  const handleChangeEndDate = (value) => {
    const formattedDate = dayjs(value).format("YYYY-MM-DD");
    changeEndDate(formattedDate);
    setEndDate(formattedDate);
    console.log("endDate", formattedDate);
  };

  const [company, setCompany] = useState("");

  useEffect(() => {
    if (tabNum == 1) {
      changeCompany(48)
      setCompany(48)
    } else {
      changeCompany("")
      setCompany("")
    }
  }, [tabNum])

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
      <LocalizationProvider dateAdapter={AdapterDayjs}>
        <Grid
          container
          sx={{ display: "flex", height: "4rem", alignItems: "center", p: 1 }}
        >
          {tabNum == 0 && <Box>
            <DemoContainer components={["DatePicker"]}>
              <DatePicker
                label="Start Date"
                slotProps={{
                  textField: {
                    size: "small",
                    error: false,
                  },
                }}
                onChange={(newDate) => handleChangeStartDate(newDate)}
                sx={{ width: "12rem" }}
              />
              <DatePicker
                label="End Date"
                slotProps={{
                  textField: {
                    size: "small",
                    error: false,
                  },
                }}
                onChange={(newDate) => handleChangeEndDate(newDate)}
                sx={{ width: "12rem" }}
              />
            </DemoContainer>
          </Box>}
          <Grid pt={1} pl={2}>
            <FormControl
              size="small"
              sx={{ backgroundColor: "white", width: "12rem" }}
            >
              <InputLabel id="demo-select-small-label">Company</InputLabel>
              <Select
                labelId="demo-select-small-label"
                id="demo-select-small"
                value={company}
                label="Company"
                onChange={handleChangeCompany}
              >
                <MenuItem value={48}>삼성</MenuItem>
                <MenuItem value={49}>SK하이닉스</MenuItem>
                <MenuItem value={50}>LG에너지솔루션</MenuItem>
                <MenuItem value={51}>기아</MenuItem>
                <MenuItem value={52}>현대자동차</MenuItem>
                <MenuItem value={53}>셀트리온</MenuItem>
                <MenuItem value={54}>POSCO홀딩스</MenuItem>
                <MenuItem value={55}>Naver</MenuItem>
                <MenuItem value={56}>LG화학</MenuItem>
                <MenuItem value={57}>삼성물산</MenuItem>
                <MenuItem value={58}>삼성SDI</MenuItem>
                <MenuItem value={59}>KB금융</MenuItem>
                <MenuItem value={60}>카카오</MenuItem>
                <MenuItem value={61}>신한지주</MenuItem>
                <MenuItem value={62}>현대모비스</MenuItem>
                <MenuItem value={63}>포스코퓨처엠</MenuItem>
                <MenuItem value={64}>하나금융지주</MenuItem>
                <MenuItem value={65}>LG전자</MenuItem>
              </Select>
            </FormControl>
          </Grid>
          <Grid pt={1} pl={2}>
            <Button
              onClick={handleChangeConfirm}
              sx={{
                height: "2rem",
                fontFamily: "GmarketSansMedium",
                fontWeight: "bold",
                color: "#397d60",
                border: "2px solid #397d60",
                borderRadius: "1.2rem",
              }}
            >
              조 회
            </Button>
          </Grid>
        </Grid>
        <Divider />
      </LocalizationProvider>
    </>
  );
}
