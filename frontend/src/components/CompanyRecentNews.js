import React from "react";
import "../css/font.css";
import "../css/layout.css";
import { Box, Typography, List, ListItem } from "@mui/material";

const newsSamsung = [
  {
    title: "삼성전자, MVC 열리는 바르셀로나서 갤S24 체험관 운영",
    summary: [
      "바르셀로나 중심지 카탈루냐 광장에 갤럭시 S24를 다채롭게 체험할 수 있는..",
      "세계 최대 모바일 전시회 '모바일 월드 콩그레스(MWC) 2024'가 열리는...",
    ],
    sentiment: "😮",
    relatedNews: "24",
    keywords: ["바르셀로나", "갤럭시 S24"],
  },
  {
    title: "삼성전자, 18년 연속 글로벌 TV 시장 1위",
    summary: [
      "2삼성전자는 지난해 글로벌 TV 시장에서 매출 기준 30.1%의 점유율을 기록하며...",
      "2지난해 삼성 QLED 제품 판매는 831만대를 판매했는데, 2017년 첫 선을 보인 이후...",
    ],
    sentiment: "😀",
    relatedNews: "32",
    keywords: ["TV", "갤럭시 QLED"],
  },
  {
    title: "'2018년 3명 사상' 삼성전자 CO2 누출 책임자 일부 유죄",
    summary: [
      "2삼성전자는 지난해 글로벌 TV 시장에서 매출 기준 30.1%의 점유율을 기록하며...",
      "2지난해 삼성 QLED 제품 판매는 831만대를 판매했는데, 2017년 첫 선을 보인 이후...",
    ],
    sentiment: "😞",
    relatedNews: "18",
    keywords: ["TV", "갤럭시 QLED"],
  },
];

export default function CompanyRecentNews() {
  return (
    <>
      {newsSamsung.map((news, idx) => (
        <Box
          key={idx}
          sx={{
            p: 2,
            mb: 2,
            border: "1px solid lightgray",
            borderRadius: "10px",
          }}
        >
          <Typography variant="h7" sx={{ p: 1, fontWeight: "bold" }}>
            "{news["title"]}"
          </Typography>

          <Box sx={{ pl: 4 }}>
            <List sx={{ listStyleType: "square" }}>
              {news["summary"].map((summary, idx) => (
                <ListItem
                  key={idx}
                  sx={{
                    p: 0.5,
                    display: "list-item",
                    fontSize: "1rem",
                    fontFamily: "omyu_pretty",
                  }}
                >
                  {summary}
                </ListItem>
              ))}
            </List>
          </Box>
          <Box
            sx={{ pl: 3, font: "0.8rem light gray", fontFamily: "omyu_pretty" }}
          >
            {news["sentiment"]} | 관련 뉴스 {news["relatedNews"]}건 |{" "}
            {news["keywords"].map((keyword, idx) => (
              <span key={idx}>#{keyword} </span>
            ))}
          </Box>
        </Box>
      ))}
    </>
  );
}
