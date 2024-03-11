import React from "react";
import "../css/font.css";
import "../css/layout.css";
import {
  Grid,
} from "@mui/material";

import CompanyRecentNews from "../components/CompanyRecentNews";

function CompanyInfo() {

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
          <CompanyRecentNews />
        </Grid>

        {/* 본문 우측 */}
        <Grid
          item
          sx={{
            width: { sm: "100%", md: "50%" },
            p: 4,
          }}
        >
        </Grid>
      </Grid >

    </>
  );
}
export default CompanyInfo;
