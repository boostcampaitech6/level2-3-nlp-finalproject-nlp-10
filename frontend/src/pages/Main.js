import React from 'react';
import { Link } from "react-router-dom";
import {
  Box,
  Grid,
  Typography,
  Divider,
  Chip,
  createTheme,
  ThemeProvider,
} from "@mui/material";
import "../css/font.css";
import { IconContext } from "react-icons";
import { BsGlobe2 } from "react-icons/bs";
import liveLogo from "../img/liveLogo.png"

const styles = (theme) => ({
  root: {
    // padding: theme.spacing(3),
    margin: 0,
    padding: 0,
    background: "#eeeeee",
  },
  box: {
    padding: theme.spacing(5),
    color: theme.pallete.text.warn,
  },
});

const theme = createTheme({
  typography: {
    fontFamily: "Black Han Sans",
  }
});


export default function Main() {
  return (
    <>
      <div className={styles.root} name="main" >
        <Divider sx={{ width: { xs: "60%", md: "63%", lg: "60%" }, borderColor: '#54cc99', mt: "3rem", mb: "1px", borderBottomWidth: 4 }} />
        <Divider sx={{ width: { sm: "60%", md: "63%", lg: "60%" }, borderColor: "black", borderBottomWidth: 3.5 }} />
        <Grid container direction="row" justifyContent="center" sx={{ width: "100%", height: "23rem", backgroundColor: "#def7ef", display: 'flex', alignItems: "center" }}>
          <ThemeProvider theme={theme}>
            <Box sx={{ width: "16rem", textAlign: 'center', fontFamily: 'Black Han Sans' }}>
              <Divider sx={{ borderColor: "black", borderBottomWidth: 4 }} />
              <Box sx={{ width: '100%' }}>
                <Typography sx={{ width: '100%', fontSize: '3rem', lineHeight: '3rem', letterSpacing: 23, overflow: "hidden", pt: 1, pl: 1.7, }}>
                  그냥보는
                </Typography>
              </Box>
              <Divider sx={{ borderColor: "black", borderBottomWidth: 4 }} />
              <Typography sx={{ fontSize: '6rem', lineHeight: '5.5rem', pt: 2, pl: 1 }}>
                뇌빼고
              </Typography>
              <Typography display="inline" sx={{ fontSize: '6rem', lineHeight: '5.5rem', pt: 2, pl: 1, pr: 1 }}>
                경
              </Typography>
              <Box
                component="img"
                src={liveLogo}
                sx={{ objectFit: "cover", width: "4rem", display: 'inline', }}
              />
              {/* <IconContext.Provider value={{ size: "4rem" }}><BsGlobe2 color='#57c1fa' /></IconContext.Provider> */}
              <Typography display="inline" sx={{ fontSize: '6rem', lineHeight: '5.5rem', pt: 2, pl: 1 }}>제</Typography>
              <Typography sx={{ fontSize: '6rem', lineHeight: '5.5rem', pl: 1 }}>
                뉘우스
              </Typography>
              <Divider sx={{ borderColor: "black", borderBottomWidth: 4 }} />
            </Box>
          </ThemeProvider>
        </Grid>
        <Divider sx={{ borderColor: "black", borderBottomWidth: 3.5 }} />
        <Box sx={{ display: "flex", justifyContent: "flex-end" }}>
          <Divider sx={{ width: { xs: "60%", md: "63%", lg: "60%" }, borderColor: '#54cc99', mt: "1px", borderBottomWidth: 4 }} />
        </Box>
        <Box display="flex" justifyContent="center" pt={3.5} >
          <Grid container justifyContent="space-evenly" sx={{ width: "60%" }}>
            <Link to="/contents" state={"0"}>
              <Chip label="오늘의 기업 뉴스" variant='outlined' sx={{ p: "20px 15px", fontFamily: "GmarketSansMedium", fontSize: "1.2rem", bgcolor: "#f3f2f2", borderRadius: "1.3rem", borderColor: "#c9c9c9", borderWidth: "1.7px" }} />
            </Link>
            <Link to="/contents" state={"1"}>
              <Chip label="실시간 기업 정보" variant='outlined' sx={{ p: "20px 15px", fontFamily: "GmarketSansMedium", fontSize: "1.2rem", bgcolor: "#f3f2f2", borderRadius: "1.3rem", borderColor: "#c9c9c9", borderWidth: "1.7px" }} />
            </Link>
            <Link to="/contents" state={"2"}>
              <Chip label="기업 리포트 생성" variant='outlined' sx={{ p: "20px 15px", fontFamily: "GmarketSansMedium", fontSize: "1.2rem", bgcolor: "#f3f2f2", borderRadius: "1.3rem", borderColor: "#c9c9c9", borderWidth: "1.7px" }} />
            </Link>
          </Grid>
        </Box>
      </div >
    </>
  )
}
