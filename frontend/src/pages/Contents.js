import React from "react";
import { useState } from "react";
import { useLocation } from "react-router-dom";
import "../css/font.css";
import "../css/layout.css";
import { Box } from "@mui/material";
import NavBar from "../components/NavBar";
import CompanyInfo from "./CompanyInfo";
import Allnews from "./Allnews";
import Report from './Report'
import FilterTab from "../components/FilterTab";

const styles = (theme) => ({
  root: {
    // padding: theme.spacing(3),
    margin: 0,
    padding: 0,
    background: "#eeeeee",
  },
  //   paper: {
  //     padding: theme.spacing(3),
  //     color: theme.pallete.text.primary,
  //   },
  //   box: {
  //     padding: theme.spacing(5),
  //     color: theme.pallete.text.warn,
  //   },
});

export default function Main() {
  const location = useLocation();
  const tabNum = location.state ? location.state : "0";
  const [value, setValue] = useState(tabNum);

  const handleChange = (e, newValue) => {
    setValue(newValue);
  };

  const [startDate, setStartDate] = useState("2023-11-01");
  const [endDate, setEndDate] = useState("2023-11-02");
  const [company, setCompany] = useState(48);
  const [confirm, setConfirm] = useState(true);
  const [startTitleId, setStartTitleId] = useState(0);

  const handleChangeStartDate = (value) => {
    setStartDate(value);
    console.log("start value", value);
  };

  const handleChangeEndDate = (value) => {
    setEndDate(value);
    console.log("end value", value);
  };

  const handleChangeCompany = (value) => {
    setCompany(value);
    console.log("company value", value);
  };

  const handleChangeConfirm = (value) => {
    setConfirm(value);
    setStartTitleId(0);
    console.log("confirm value", value);
    console.log("title id: ", startTitleId);
  };

  return (
    <>
      <div className={styles.root} name="main">
        <NavBar selectedTab={value} onClickTab={handleChange} />
        {value != "2" && <FilterTab
          changeStartDate={handleChangeStartDate}
          changeEndDate={handleChangeEndDate}
          changeCompany={handleChangeCompany}
          changeConfirm={handleChangeConfirm}
          tabNum={value}
        />}
        {value == "0" && (
          <Allnews
            startDate={startDate}
            endDate={endDate}
            company={company}
            confirm={confirm}
            startTitleId={startTitleId}
          />
        )}
        {value == "1" && (
          <CompanyInfo
            startDate={startDate}
            endDate={endDate}
            company={company}
            confirm={confirm}
            tabNum={value}
          />
        )}
        {value == "2" && <Report />}
      </div>
    </>
  );
}
