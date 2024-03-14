import { React, useEffect, useState } from "react";
import "../css/font.css";
import "../css/layout.css";
import { Box, Typography, List, ListItem } from "@mui/material";
import { IoLogoDesignernews } from "react-icons/io5";
import { IconContext } from "react-icons";
import axios from "axios";

const news = [
  "5년 타면 유류비 800만원 절약…아이오닉6, 美서 일냈다",
  "4일 현대차에 따르면 아이오닉6 롱레인지 후륜 모델(18인치 휠, 복합연비 140MPGe)은 ",
  "이 아파트는 1998년 준공한 4509가구 규모 대단지 아파트다. 지하철 4호선과 우이신설경전철이 ",
];
const news_recent = [
  "5년 타면 유류비 800만원 절약…아이오닉6, 美서 일냈다",
  "4일 현대차에 따르면 아이오닉6 롱레인지 후륜 모델(18인치 휠, 복합연비 140MPGe)은 ",
  "이 아파트는 1998년 준공한 4509가구 규모 대단지 아파트다. 지하철 4호선과 우이신설경전철이 ",
  "윤 대통령은 기계·금속 등 대구가 강점이 있는 전통 산업 토대 위에 로봇, 미래 모빌리티 산업을 집중 육성하겠다고 밝혔다",
  "또한 수성 알파시티를 국가 디지털혁신지구로 지정해 제조업과 디지털의 융합을 이끄는 R&D의 핵심 거점으로 만들겠다고 말했다.",
];

export default function TopNews(props) {
  let date = "최신";
  let news_num = "3";
  if (props.date == "today") {
    date = "오늘의";
  } else if (props.date == "yesterday") {
    date = "어제의";
  } else {
    news_num = "5";
  }
  return (
    <>
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
          뉴스 Top5
        </Typography>
      </Box>

      {/* 뉴스 기사 제목 */}
      <List sx={{ p: 1, pl: 2.5, listStyleType: "square" }}>
        {props.title.slice(0, 5).map((it, idx) => (
          <ListItem
            key={idx}
            sx={{
              display: "list-item",
              p: 0.5,
              fontSize: "1.5rem",
              fontFamily: "omyu_pretty",
            }}
          >
            {it}
          </ListItem>
        ))}
      </List>
    </>
  );
}
