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
                MenuProps={{ PaperProps: { sx: { maxHeight: 300 } } }}
              >
                {companyNames.map((company, idx) => (
                  <MenuItem value={idx + 48}>{company}</MenuItem>
                ))}
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
