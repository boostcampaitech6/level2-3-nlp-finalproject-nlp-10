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

const news = [
  "5년 타면 유류비 800만원 절약…아이오닉6, 美서 일냈다",
  "4일 현대차에 따르면 아이오닉6 롱레인지 후륜 모델(18인치 휠, 복합연비 140MPGe)은 ",
  "이 아파트는 1998년 준공한 4509가구 규모 대단지 아파트다. 지하철 4호선과 우이신설경전철이 ",
];

const title = "삼성전자, MVC 열리는 바르셀로나서 갤S24 체험관 운영";

const tag = ["언급량 1위", "매우 긍정적", "TV", "OLED"];

const newsList = [
  "대만 TSMC는 지난해 애리조나주에 건설 중인 반도체 1공장 가동 시기를 2024년에서 2025년으로 미뤘다. 2공장 생산 시점은 2026년에서 2027년 이후로 늦췄다. ",
  "인텔이 오하이오주에 건설 중인 200억달러(약 26조6000억원)규모의 반도체 공장의 가동 시기도 당초 2025년에서 2026년으로 지연된 것으로 알려졌다.",
  "미국 노동통계국에 따르면 지난해 말 신규 산업 건물 건설 지수는 2019년 137.4(2007년=100)에서 2022년 191.4로 39.4% 급등했다. 전기를 조절하는데 쓰인 스위치 기어와 변압기 등 부품은 납품에 100주 이상 걸리는 경우도 있다. ",
  "3일 한국거래소에 따르면 지난주 삼성전자는 7만3400원에 거래를 마쳤습니다. 올 들어 주가가 7.8% 떨어졌습니다. 작년 5월 말부터 7만원 박스권에 갇혔습니다.",
];

function Companynews() {
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
          {/* 상단 */}
          <Grid
            item
            xs={12}
            sx={{
              height: "20%",
              // border: "1px solid black",
            }}
            spacing={0}
          >
            <Box
              className={styles.paper}
              sx={{ backgroundColor: "rgb(218, 248, 240)", height: "100%" }}
            >
              {/* 상단 좌측 버튼 (실시간 기업 정보, ...) */}
              <Box sx={{ p: 3 }}>
                <Grid container sx={{}}>
                  <Grid sm={1} xs={12} sx={{ p: 0.8 }}>
                    <Button
                      variant="outlined"
                      sx={{
                        p: 0.5,
                        width: "90%",
                        backgroundColor: "white",
                        color: "gray",
                      }}
                    >
                      <Typography
                        sx={{
                          fontFamily: "omyu_pretty",
                          textAlign: "center",
                          fontFamily: "KOTRAHOPE",
                        }}
                      >
                        {tab[1]}
                      </Typography>
                    </Button>
                  </Grid>
                  <Grid sm={1} xs={12} sx={{ p: 0.8 }}>
                    <Button
                      variant="outlined"
                      sx={{
                        p: 0.5,
                        width: "90%",
                        backgroundColor: "white",
                        color: "gray",
                      }}
                    >
                      <Typography
                        sx={{
                          fontFamily: "omyu_pretty",
                          textAlign: "center",
                          fontFamily: "KOTRAHOPE",
                        }}
                      >
                        {tab[0]}
                      </Typography>
                    </Button>
                  </Grid>
                  <Grid sm={1} xs={12} sx={{ p: 0.8 }}>
                    <Button
                      variant="outlined"
                      sx={{
                        p: 0.5,
                        width: "90%",
                        backgroundColor: "white",
                        color: "gray",
                      }}
                    >
                      <Typography
                        sx={{
                          fontFamily: "omyu_pretty",
                          textAlign: "center",
                          fontFamily: "KOTRAHOPE",
                        }}
                      >
                        {tab[2]}
                      </Typography>
                    </Button>
                  </Grid>
                  {/* <Grid sm={3}>
                    <Box
                      sx={{
                        display: "flex",
                        flexDirection: "column",
                        alignItems: "center",
                        "& > *": {
                          m: 1,
                        },
                      }}
                    >
                      <ButtonGroup
                        variant="outlined"
                        aria-label="Basic button group"
                      >
                        <Button sx={{ backgroundColor: "white", pl: 5, pr: 5 }}>
                          {tab[1]}
                        </Button>
                        <Box sx={{ p: 1 }}></Box>
                        <Button sx={{ backgroundColor: "white", pl: 5, pr: 5 }}>
                          {tab[0]}
                        </Button>
                        <Box sx={{ p: 1 }}></Box>
                        <Button sx={{ backgroundColor: "white", pl: 5, pr: 5 }}>
                          {tab[2]}
                        </Button>
                      </ButtonGroup>
                    </Box>
                  </Grid> */}
                  <Grid sm={7}></Grid>

                  {/* 우측 상단 dropout (date, company) */}
                  <Grid sm={2}>
                    <Box sx={{ display: "flex", pt: 0 }}>
                      <Grid container sx={{ pt: 0 }}>
                        <Grid sm={6} xs={12} sx={{ p: 0.8, pt: 0 }}>
                          <Box sx={{ minWidth: 50, p: 1 }}>
                            <FormControl
                              fullWidth
                              sx={{ backgroundColor: "white" }}
                            >
                              <InputLabel id="demo-simple-select-label">
                                Date
                              </InputLabel>
                              <Select
                                labelId="demo-simple-select-label"
                                id="demo-simple-select"
                                value={date}
                                label="Date"
                                onChange={handleChangeDate}
                              >
                                <MenuItem value={10}>하루</MenuItem>
                                <MenuItem value={20}>일주일</MenuItem>
                                <MenuItem value={30}>한 달</MenuItem>
                              </Select>
                            </FormControl>
                          </Box>
                        </Grid>
                        <Grid sm={6} xs={12} sx={{ p: 0.8, pt: 0 }}>
                          <Box sx={{ minWidth: 50, p: 1 }}>
                            <FormControl
                              fullWidth
                              sx={{ backgroundColor: "white" }}
                            >
                              <InputLabel id="demo-simple-select-label">
                                Company
                              </InputLabel>
                              <Select
                                labelId="demo-simple-select-label"
                                id="demo-simple-select"
                                value={company}
                                label="Company"
                                onChange={handleChangeCompany}
                              >
                                <MenuItem value={10}>삼성</MenuItem>
                                <MenuItem value={20}>LG에너지솔루션</MenuItem>
                                <MenuItem value={30}>SK 하이닉스</MenuItem>
                              </Select>
                            </FormControl>
                          </Box>
                        </Grid>
                        <Grid sm={8} xs={6} sx={{ p: 0.8 }}></Grid>
                      </Grid>
                    </Box>
                  </Grid>
                </Grid>
              </Box>
            </Box>
          </Grid>

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
                <Box sx={{ display: "flex" }}>
                  <IconContext.Provider value={{ size: "25px" }}>
                    <IoLogoDesignernews />
                  </IconContext.Provider>
                  <Typography
                    variant="h5"
                    sx={{
                      fontFamily: "KOTRAHOPE",
                      fontWeight: "normal",
                      pl: 1.3,
                    }}
                  >
                    오늘의 뉴스 Top3
                  </Typography>
                </Box>

                {/* 뉴스 기사 제목 */}
                <Box sx={{ p: 2 }}>
                  <Paper className={styles.paper} sx={{ minHeight: "150px" }}>
                    <Box sx={{ p: 1.5 }}>
                      {news.map((it) => (
                        <Typography sx={{ p: 0.3, fontFamily: "omyu_pretty" }}>
                          - {it}
                        </Typography>
                      ))}
                    </Box>
                  </Paper>
                </Box>

                {/* 어제의 뉴스 제목 */}

                <Box sx={{ display: "flex", mt: 3 }}>
                  <IconContext.Provider value={{ size: "25px" }}>
                    <FaBackward />
                  </IconContext.Provider>
                  <Typography
                    variant="h5"
                    sx={{
                      fontFamily: "KOTRAHOPE",
                      fontWeight: "normal",
                      pl: 1.3,
                    }}
                  >
                    어제의 뉴스 Top3
                  </Typography>
                </Box>

                {/*어제의 뉴스 기사 제목 */}
                <Box sx={{ p: 2 }}>
                  <Paper className={styles.paper} sx={{ minHeight: "150px" }}>
                    <Box sx={{ p: 1.5 }}>
                      {news.map((it) => (
                        <Typography sx={{ p: 0.3, fontFamily: "omyu_pretty" }}>
                          - {it}
                        </Typography>
                      ))}
                    </Box>
                  </Paper>
                </Box>

                {/* 다이어그램 */}

                <Box sx={{ display: "flex", mt: 3 }}>
                  <IconContext.Provider value={{ size: "25px" }}>
                    <VscSymbolKeyword />
                  </IconContext.Provider>
                  <Typography
                    variant="h5"
                    sx={{
                      fontFamily: "KOTRAHOPE",
                      fontWeight: "normal",
                      pl: 1.3,
                      pb: 1.3,
                    }}
                  >
                    오늘의 키워드
                  </Typography>
                </Box>

                <Box sx={{ p: 1 }}>
                  <Paper
                    elevation={3}
                    // className={styles.paper}
                    // elevation={0}
                    sx={{
                      minHeight: "200px",
                      // borderRadius: "20px",
                      // border: "5px solid rgb(218, 248, 240)",
                    }}
                  >
                    <Box
                      component="img"
                      src={diagram}
                      sx={{
                        objectFit: "cover",
                        width: "100%",
                        height: "100%",
                      }}
                    />
                  </Paper>
                </Box>
              </Box>
            </Paper>
            <Grid sm={12}>
              <Box sx={{ minHeight: "30px" }}></Box>
            </Grid>
          </Grid>

          {/* 본문 우측 */}
          <Grid
            item
            sm={6}
            xs={12}
            sx={{
              // border: "1px solid red",
              height: "85%",
              display: "flex",
              flexDirection: "column",
            }}
          >
            <Paper
              className={styles.paper}
              sx={{
                flex: "1",
                // backgroundColor: "#f8f9fa"
              }}
              elevation={3}
            >
              <Box sx={{ p: 5, pt: 3 }}>
                <Paper
                  elevation={0}
                  sx={{
                    p: 1.5,
                    backgroundColor: "rgb(218, 248, 240)",
                  }}
                >
                  {/* 제목 */}
                  <Typography
                    sx={{
                      // color: "white",
                      fontFamily: "KOTRAHOPE",
                      textAlign: "center",
                    }}
                  >
                    " {title} "
                  </Typography>
                </Paper>
                <Paper
                  // className={styles.paper}
                  // elevation={0}
                  sx={{
                    minHeight: "200px",
                    width: "70%",
                    height: "100%",
                    margin: "auto",
                    display: "block",
                    mt: 5,
                    // borderRadius: "20px",
                    // border: "5px solid rgb(218, 248, 240)",
                  }}
                >
                  {/* 요약 뉴스 이미지 */}
                  <Box
                    component="img"
                    src={samsung}
                    sx={{
                      objectFit: "cover",
                      width: "100%",
                      height: "100%",
                    }}
                  />
                </Paper>
                {/* 키워드 */}
                <Box
                  sx={{
                    p: 2,
                  }}
                >
                  <Grid container>
                    {tag.map((it) => (
                      <Grid sm={3} sx={{ p: 0.8 }}>
                        <Paper sx={{ p: 0.5 }}>
                          <Typography
                            sx={{
                              fontFamily: "omyu_pretty",
                              textAlign: "center",
                              color: "#3f50b5",
                            }}
                          >
                            # {it}
                          </Typography>
                        </Paper>
                      </Grid>
                    ))}
                  </Grid>
                </Box>
                {/* 뉴스 요약 */}
                <Box sx={{ p: 2 }}>
                  <Paper className={styles.paper} sx={{ minHeight: "200px" }}>
                    <Box sx={{ p: 1.5 }}>
                      {newsList.map((it) => (
                        <Typography
                          variant="h6"
                          sx={{ p: 0.3, fontFamily: "omyu_pretty" }}
                        >
                          - {it}
                        </Typography>
                      ))}
                    </Box>
                  </Paper>
                </Box>
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
export default Companynews;
