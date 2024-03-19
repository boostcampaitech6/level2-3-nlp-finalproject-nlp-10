import React from 'react'

import {
  Box,
  Tab,
  Tabs,
} from "@mui/material";

function NavBar(props) {
  //const [selectedTab, onClickTab] = props;
  return (
    <>
      <Box sx={{ width: '100%', color: 'gray', backgroundColor: "#def7ef" }}>
        <Tabs sx={{ height: "1.5rem", pl: "10px", ".MuiTab-root": { pt: "15px", fontFamily: "GmarketSansMedium", fontSize: "1.3rem" }, ".Mui-selected": { color: '#090b0a' } }} value={props.selectedTab} onChange={props.onClickTab} TabIndicatorProps={{ style: { background: '#54cc99' } }}>
          <Tab label="오늘의 기업 뉴스" value="0" />
          <Tab label="실시간 기업 정보" value="1" />
          <Tab label="기업 리포트 생성" value="2" />
        </Tabs>
      </Box>
    </>
  )
}

export default NavBar