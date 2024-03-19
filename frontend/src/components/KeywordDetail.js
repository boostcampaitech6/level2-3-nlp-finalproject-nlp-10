import React from 'react'
import "../css/font.css";
import "../css/layout.css";
import {
  Box,
  Grid,
  Typography,
  List,
  ListItem,
  Chip,
} from "@mui/material";
import samsung from "../img/samsung.png";

export default function KeywordDetail() {
  let title = "삼성전자, MVC 열리는 바르셀로나서 갤S24 체험관 운영";
  let tag = ["언급량 1위", "매우 긍정적", "TV", "OLED"];
  let newsList = [
    "대만 TSMC는 지난해 애리조나주에 건설 중인 반도체 1공장 가동 시기를 2024년에서 2025년으로 미뤘다. 2공장 생산 시점은 2026년에서 2027년 이후로 늦췄다. ",
    "인텔이 오하이오주에 건설 중인 200억달러(약 26조6000억원)규모의 반도체 공장의 가동 시기도 당초 2025년에서 2026년으로 지연된 것으로 알려졌다.",
    "미국 노동통계국에 따르면 지난해 말 신규 산업 건물 건설 지수는 2019년 137.4(2007년=100)에서 2022년 191.4로 39.4% 급등했다. 전기를 조절하는데 쓰인 스위치 기어와 변압기 등 부품은 납품에 100주 이상 걸리는 경우도 있다. ",
    "3일 한국거래소에 따르면 지난주 삼성전자는 7만3400원에 거래를 마쳤습니다. 올 들어 주가가 7.8% 떨어졌습니다. 작년 5월 말부터 7만원 박스권에 갇혔습니다.",
  ];

  return (
    <>

      <Box sx={{ p: 1.5, backgroundColor: "rgb(218, 248, 240)", }}>
        {/* 제목 */}
        <Typography sx={{ fontFamily: "KOTRAHOPE", textAlign: "center", }}        >
          " {title} "
        </Typography>
      </Box>
      <Box sx={{ minHeight: "200px", width: "80%", margin: "auto", display: "block", padding: 4, }}>
        {/* 요약 뉴스 이미지 */}
        <Box
          component="img"
          src={samsung}
          sx={{ objectFit: "cover", width: "100%", height: "100%", }}
        />
      </Box>
      {/* 키워드 */}
      <Grid container>
        {tag.map((it, idx) => (
          <Box key={idx} sx={{ pr: 2 }}>
            <Chip label={`# ${it}`}
              sx={{
                fontFamily: "omyu_pretty",
                textAlign: "center",
              }}
            />
          </Box>
        ))}
      </Grid>
      {/* 뉴스 요약 */}
      <List sx={{ pl: 2.5, listStyleType: 'square' }}>
        {newsList.map((it, idx) => (
          <ListItem key={idx} sx={{ display: 'list-item', p: 1, fontSize: "1rem", fontFamily: "omyu_pretty" }}                  >
            {it}
          </ListItem>
        ))}
      </List>
    </>
  )
}
