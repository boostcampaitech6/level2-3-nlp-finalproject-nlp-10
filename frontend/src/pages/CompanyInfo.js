import React from "react";
import { useState, useEffect } from "react";
import "../css/font.css";
import "../css/layout.css";
import { Grid } from "@mui/material";
import { RxDoubleArrowDown, RxDoubleArrowUp } from "react-icons/rx";
import axios from "axios";

import CompanyRecentNews from "../components/CompanyRecentNews";
import StockInfo from "../components/StockInfo";
import SentimentInfo from "../components/SentimentInfo";

function CompanyInfo({ company, confirm }) {
  const [cnt, setCnt] = useState([]);
  const [newsId, setNewsId] = useState([]);
  const [newsTitle, setNewsTitle] = useState([]);
  const [summary, setSummary] = useState([]);
  const [sentiment, setSentiment] = useState([]);
  const [companyId, setCompanyId] = useState(48);

  useEffect(() => {
    const company_id = 48;
    const fetchGetNews = async () => {
      try {
        const response = await axios.get(
          `http://localhost:8000/jh/get-recent-news`,
          // `${process.env.REACT_APP_SERVER_URL}/jh/get-recent-news`,
          {
            params: {
              company_id: company ? company : company_id,
            },
            // JSON.stringify(params),
          }
        );
        console.log("news제목 요약 불러오기", response.data);
        setCnt(response.data.map((item) => item.cnt));
        setNewsId(response.data.map((item) => item.news_id));
        setNewsTitle(response.data.map((item) => item.news_title));
        setSummary(response.data.map((item) => item.summary));
        setSentiment(response.data.map((item) => item.sentiment));
      } catch (err) {
        console.log("news제목 요약 불러오기 에러");
      }
    };
    fetchGetNews();
    setCompanyId(company)
  }, [confirm]);

  const [isBottom, setIsBottom] = useState(false);
  const [isTop, setIsTop] = useState(true);

  const handleScroll = (e) => {
    if (Math.abs(e.target.scrollHeight - e.target.clientHeight - e.target.scrollTop) < 1) {
      setIsBottom(true)
      setIsTop(false)
    }
    else if (e.currentTarget.scrollTop === 0) {
      setIsTop(true)
      setIsBottom(false)
    }
  }

  return (
    <>
      {/* 전체 */}
      <Grid
        container
        alignContent={"space-around"}
        sx={{ flexDirection: { sm: "column", md: "row" } }}
      >
        {/* 본문 좌측 */}
        <Grid
          item
          sx={{
            width: { sm: "100%", md: "50%" },
            display: "flex",
            flexDirection: "column",
            p: 4,
            borderRight: { md: "1px solid lightgray" },
          }}
        >
          <Grid onScroll={handleScroll} sx={{ height: "66vh", overflowY: "scroll", "&-ms-overflow-style": "none", "&::-webkit-scrollbar": { display: "none" } }}>
            <CompanyRecentNews
              cnt={cnt}
              newsId={newsId}
              newsTitle={newsTitle}
              summary={summary}
              sentiment={sentiment}
            />
          </Grid>
          <Grid sx={{ height: "4vh", display: "flex", justifyContent: "center", pt: 2, fontSize: "1.3rem", }}>
            {isBottom && <RxDoubleArrowUp color="#a1a1a1" />}
            {isTop && <RxDoubleArrowDown color="#a1a1a1" />}
          </Grid>
        </Grid>

        {/* 본문 우측 */}
        <Grid
          item
          sx={{
            width: { sm: "100%", md: "50%" },
            display: "flex",
            flexDirection: "column",
          }}
        >
          <Grid height={"35vh"} >
            <StockInfo />
          </Grid>
          <Grid height={"35vh"} >
            <SentimentInfo
              companyId={companyId}
            />
          </Grid>
        </Grid>
      </Grid>
    </>
  );
}
export default CompanyInfo;
