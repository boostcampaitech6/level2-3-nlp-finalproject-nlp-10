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

function CompanyInfo({ startDate, endDate, company, confirm }) {
  const [cnt, setCnt] = useState([]);
  const [topicId, setTopicId] = useState([]);
  const [topicTitleSummary, setTopicTitleSummary] = useState([]);
  const [topicSummary, setTopicSummary] = useState([]);
  const [title, setTitle] = useState([]);
  const [sentiment, setSentiment] = useState([]);
  const [companyId, setCompanyId] = useState(48);

  useEffect(() => {
    const start_date = "2023-11-01";
    const end_date = "2023-11-02";
    const company_id = 1;
    const fetchGetNews = async () => {
      try {
        const response = await axios.get(
          `${process.env.REACT_APP_SERVER_URL}/jh/get-titles`,
          {
            params: {
              start_date: startDate,
              end_date: endDate,
              company_id: company,
            },
            // JSON.stringify(params),
          }
        );
        console.log("news제목 요약 불러오기", response.data);
        setCnt(response.data.map((item) => item.cnt));
        setTopicId(response.data.map((item) => item.topic_id));
        setTopicTitleSummary(
          response.data.map((item) => item.topic_title_summary)
        );
        setTopicSummary(response.data.map((item) => item.topic_summary));
        setTitle(response.data.map((item) => item.title));
        setSentiment(response.data.map((item) => item.sentiment));
      } catch (err) {
        console.log("news제목 요약 불러오기 에러");
      }
    };
    fetchGetNews();
    setCompanyId(company)
  }, [confirm]);

  const [isBottom, setIsBottom] = useState(false);

  const handleScroll = (e) => {
    if (Math.abs(e.target.scrollHeight - e.target.clientHeight - e.target.scrollTop) < 1) { setIsBottom(true) }
    else setIsBottom(false);
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
              topicId={topicId}
              topicTitleSummary={topicTitleSummary}
              topicSummary={topicSummary}
              title={title}
              sentiment={sentiment}
            />
          </Grid>
          <Grid sx={{ height: "4vh", display: "flex", justifyContent: "center", pt: 2, fontSize: "1.3rem", }}>
            {isBottom ? <RxDoubleArrowUp color="#a1a1a1" /> : <RxDoubleArrowDown color="#a1a1a1" />}
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
