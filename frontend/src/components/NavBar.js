import React from 'react'
import { Link } from "react-router-dom";
import {
  Grid,
  Box,
  Tab,
  Tabs,
} from "@mui/material";
import {
  createTheme,
  ThemeProvider,
} from "@mui/material/styles";
import liveLogo from "../img/liveLogo.png"

function NavBar(props) {

  const styles = (theme) => ({
    root: {
      MuiSelected: {
        "color": "black"
      }
    }
  });

  const theme = createTheme({
    components: { MuiTab: { styleOverrides: { root: { pt: "15px", fontFamily: "GmarketSansMedium", fontSize: "1.3rem", "&.Mui-selected": { color: "black" } } } } }
  });
  return (
    <>
      <Grid sx={{ width: '100%', display: "flex", alignItems: "center", color: 'gray', backgroundColor: "#def7ef" }}>
        <Link to="/">
          <Box
            component="img"
            src={liveLogo}
            sx={{ objectFit: "cover", width: "2rem", pl: 2, pt: 1, pr: 2 }}
          />
        </Link>
        <ThemeProvider theme={theme}>
          <Tabs value={props.selectedTab} onChange={props.onClickTab} TabIndicatorProps={{ style: { background: '#54cc99' } }}>
            <Tab label="오늘의 기업 뉴스" value="0" />
            <Tab label="실시간 기업 정보" value="1" />
            <Tab label="기업 리포트 생성" value="2" />
          </Tabs>
        </ThemeProvider>
      </Grid>
    </>
  )
}

export default NavBar