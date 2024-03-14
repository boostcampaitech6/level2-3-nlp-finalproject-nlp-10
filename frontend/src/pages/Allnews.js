import React from "react";
import { useState, useEffect } from "react";
import "../css/font.css";
import "../css/layout.css";
import { Grid } from "@mui/material";
import TopNews from "../components/TopNews";
import KeywordChart from "../components/KeywordChart";
import KeywordDetail from "../components/KeywordDetail";
import axios from "axios";

function Allnews({ startDate, endDate, company, confirm }) {
  // const [date, setDate] = useState("");

  // const handleChangeDate = (event) => {
  //   setDate(event.target.value);
  // };

  // const [company, setCompany] = useState("");

  // const handleChangeCompany = (event) => {
  //   setCompany(event.target.value);
  // };

  const [cnt, setCnt] = useState([]);
  const [topicId, setTopicId] = useState([]);
  const [topicTitleSummary, setTopicTitleSummary] = useState([]);
  const [topicSummary, setTopicSummary] = useState([]);
  const [title, setTitle] = useState([]);

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
      } catch (err) {
        console.log("news제목 요약 불러오기 에러");
      }
    };
    fetchGetNews();
  }, [confirm]);

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
          {/* 오늘 뉴스 */}
          <TopNews
            date={"today"}
            cnt={cnt}
            topicId={topicId}
            topicSummary={topicSummary}
            topicTitleSummary={topicTitleSummary}
            title={title}
          />

          {/* 다이어그램 */}
          <KeywordChart
            date={"today"}
            cnt={cnt}
            topicId={topicId}
            topicSummary={topicSummary}
            topicTitleSummary={topicTitleSummary}
            title={title}
          />
          {/*어제 뉴스*/}
          {/* <TopNews date={'yesterday'} /> */}
        </Grid>

        {/* 본문 우측 */}
        <Grid
          item
          sx={{
            width: { sm: "100%", md: "50%" },
            p: 4,
          }}
        >
          <KeywordDetail />
        </Grid>
      </Grid>
    </>
  );
}
export default Allnews;
