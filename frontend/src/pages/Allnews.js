import React from "react";
import { useState } from "react";
import "../css/font.css";
import "../css/layout.css";
import { Grid } from "@mui/material";
import TopNews from "../components/TopNews";
import KeywordChart from "../components/KeywordChart";
import KeywordDetail from "../components/KeywordDetail";

function Allnews() {
  // const [date, setDate] = useState("");

  // const handleChangeDate = (event) => {
  //   setDate(event.target.value);
  // };

  // const [company, setCompany] = useState("");

  // const handleChangeCompany = (event) => {
  //   setCompany(event.target.value);
  // };

  return (
    <>
      {/* 전체 */}
      <Grid container alignContent={"space-around"} sx={{ flexDirection: { sm: "column", md: "row" } }}>

        {/* 본문 좌측 */}
        <Grid
          item
          sx={{
            width: { sm: "100%", md: "50%" },
            display: "flex",
            flexDirection: "column",
            p: 4,
            borderRight: { md: '1px solid lightgray' }
          }}
        >
          {/* 오늘 뉴스 */}
          <TopNews date={'today'} />

          {/* 다이어그램 */}
          <KeywordChart />
          {/*어제 뉴스*/}
          <TopNews date={'yesterday'} />

        </Grid>


        {/* 본문 우측 */}
        <Grid
          item
          sx={{
            width: { sm: "100%", md: "50%" },
            p: 4,
          }}
        >
          <KeywordDetail />
        </Grid>
      </Grid >
    </>
  );
}
export default Allnews;
