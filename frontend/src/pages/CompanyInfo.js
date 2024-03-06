import React from "react";
import { useState } from "react";
import "../css/font.css";
import "../css/layout.css";
import {
  Box,
  createTheme,
  Grid,
  Container,
  Typography,
  Paper,
  InputLabel,
  MenuItem,
  FormControl,
  Select,
  Button,
  ButtonGroup,
} from "@mui/material";
import NavBar from "../components/NavBar"
import { IoLogoDesignernews } from "react-icons/io5";
import { IconContext } from "react-icons";
import { FaBackward } from "react-icons/fa6";
import { VscSymbolKeyword } from "react-icons/vsc";

import diagram from "../img/diagram.png";
import samsung from "../img/samsung.png";

const styles = (theme) => ({
  root: {
    // padding: theme.spacing(3),
    margin: 0,
    padding: 0,
    background: "#eeeee",
  },
  paper: {
    padding: theme.spacing(3),
    color: theme.pallete.text.primary,
  },
  box: {
    padding: theme.spacing(5),
    color: theme.pallete.text.warn,
  },
});

const tab = ["오늘 기업 뉴스", "실시간 기업정보", "리포트 생성"];

const news_samsung = {
  "삼성전자, MVC 열리는 바르셀로나서 갤S24 체험관 운영": [
    "바르셀로나 중심지 카탈루냐 광장에 갤럭시 S24를 다채롭게 체험할 수 있는..",
    "세계 최대 모바일 전시회 '모바일 월드 콩그레스(MWC) 2024'가 열리는..."
  ],
  "삼성전자, 18년 연속 글로벌 TV 시장 1위": [
    "삼성전자는 지난해 글로벌 TV 시장에서 매출 기준 30.1%의 점유율을 기록하며...",
    "지난해 삼성 QLED 제품 판매는 831만대를 판매했는데, 2017년 첫 선을 보인 이후..."
  ],
  "'2018년 3명 사상' 삼성전자 CO2 누출 책임자 일부 유죄": [
    "2삼성전자는 지난해 글로벌 TV 시장에서 매출 기준 30.1%의 점유율을 기록하며...",
    "2지난해 삼성 QLED 제품 판매는 831만대를 판매했는데, 2017년 첫 선을 보인 이후..."
  ],
};

const tag = ["언급량 1위", "매우 긍정적", "TV", "OLED"];


function CompanyInfo() {
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
      <div className={styles.root} name="main">
        {/* 전체 */}
        <Grid container spacing={3} sx={{ height: "100vh" }}>


          {/* 본문 좌측 */}
          <Grid
            item
            sm={6}
            xs={12}
            sx={{
              // border: "1px solid blue",
              height: "70%",
              display: "flex",
              flexDirection: "column",
              pt: 0,
            }}
          >
            <Paper
              className={styles.paper}
              sx={{ flex: "1", pt: 0 }}
              elevation={3}
            >
              {/* 제목 */}
              <Box sx={{ p: 5, pt: 2 }}>
                {Object.keys(news_samsung).map((title) =>
                  <div>
                    <Box sx={{ display: "flex" }}>
                      <Typography
                        variant="h7"
                        sx={{
                          fontWeight: "bold",
                          pl: 1.3,
                        }}
                      >
                        {title}
                      </Typography>
                    </Box>

                    <Box sx={{ p: 2 }}>
                      <Paper className={styles.paper} sx={{ minHeight: "150px" }}>
                        <Box sx={{ p: 1.5 }}>
                          {news_samsung[title].map((summary) => (
                            <Typography sx={{ p: 0.3, fontFamily: "omyu_pretty" }}>
                              - {summary}
                            </Typography>
                          ))}
                        </Box>
                      </Paper>
                    </Box>
                  </div>
                )}

              </Box>
            </Paper>
            <Grid sm={12}>
              <Box sx={{ minHeight: "30px" }}></Box>
            </Grid>
          </Grid>

        </Grid>
      </div>
    </>
  );
}
export default CompanyInfo;
