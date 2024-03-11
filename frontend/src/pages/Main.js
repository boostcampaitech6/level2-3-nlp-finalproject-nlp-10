import React from 'react';
import { Link } from "react-router-dom";
import {
  Box,
  Grid,
  Typography,
  Divider,
  Chip,
} from "@mui/material";
import "../css/font.css";

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

export default function Main() {
  return (
    <>
      <div className={styles.root} name="main" >
        <Divider sx={{ width: { xs: "60%", md: "63%", lg: "60%" }, borderColor: '#54cc99', mt: "3rem", mb: "1px", borderBottomWidth: 4 }} />
        <Divider sx={{ width: { sm: "60%", md: "63%", lg: "60%" }, borderColor: "black", borderBottomWidth: 3.5 }} />
        <Grid container direction="row" justifyContent="center" sx={{ width: "100%", height: "23rem", backgroundColor: "#def7ef", display: 'flex', alignItems: "center" }}>
          <Box sx={{ width: "16rem", textAlign: 'center', fontFamily: 'Black_Han_Sans' }}>
            <Divider sx={{ borderColor: "black", borderBottomWidth: 4 }} />
            <Typography sx={{ fontSize: '3rem', lineHeight: '4rem' }}>
              그냥보는
            </Typography>
            <Divider sx={{ borderColor: "black", borderBottomWidth: 4 }} />
            <Typography sx={{ fontSize: '4.5rem', lineHeight: '5rem', padding: '10px' }}>
              뇌빼고
              <br />
              경&nbsp;&nbsp;&nbsp;제
              <br />
              뉘우스
            </Typography>
            <Divider sx={{ borderColor: "black", borderBottomWidth: 4 }} />
          </Box>
        </Grid>
        <Divider sx={{ borderColor: "black", borderBottomWidth: 3.5 }} />
        <Box sx={{ display: "flex", justifyContent: "flex-end" }}>
          <Divider sx={{ width: { xs: "60%", md: "63%", lg: "60%" }, borderColor: '#54cc99', mt: "1px", borderBottomWidth: 4 }} />
        </Box>
        <Box display="flex" justifyContent="center" pt={3.5} >
          <Grid container justifyContent="space-evenly" sx={{ width: "60%" }}>
            <Link to="/contents" state={"0"}>
              <Chip label="오늘의 기업 뉴스" variant='outlined' sx={{ p: "20px 15px", fontSize: "1.2rem", fontWeight: "bold", bgcolor: "#ececec", borderRadius: "1.3rem" }} />
            </Link>
            <Link to="/contents" state={"1"}>
              <Chip label="실시간 기업 정보" variant='outlined' sx={{ p: "20px 15px", fontSize: "1.2rem", fontWeight: "bold", bgcolor: "#ececec", borderRadius: "1.3rem" }} />
            </Link>
            <Link to="/contents" state={"2"}>
              <Chip label="기업 리포트 생성" variant='outlined' sx={{ p: "20px 15px", fontSize: "1.2rem", fontWeight: "bold", bgcolor: "#ececec", borderRadius: "1.3rem" }} />
            </Link>
          </Grid>
        </Box>
      </div >
    </>
  )
}
