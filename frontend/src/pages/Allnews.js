import React from "react";
import { useState, useEffect } from "react";
import "../css/font.css";
import "../css/layout.css";
import { Grid } from "@mui/material";
import TopNews from "../components/TopNews";
import KeywordChart from "../components/KeywordChart";
import NewsDetail from "../components/NewsDetail";
import axios from "axios";

function Allnews({ startDate, endDate, company, confirm, startTitleId }) {
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
  const [sentiment, setSentiment] = useState([]);
  const [titleId, setTitleId] = useState(startTitleId);
  const [diagram, setDiagram] = useState([]);

  useEffect(() => {
    const start_date = "2023-11-01";
    const end_date = "2023-11-02";
    const company_id = 48;
    const fetchGetNews = async () => {
      try {
        const response = await axios.get(
          `http://localhost:8000/jh/get-titles`,
          // `${process.env.REACT_APP_SERVER_URL}/jh/get-titles`,
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
        setTitleId(0);
        setSentiment(response.data.map((item) => item.sentiment));

        // const newDiagram = topicTitleSummary
        //   .slice(0, 5)
        //   .map((topic, index) => ({
        //     name: topic,
        //     children: [{ name: topic, size: cnt[index] }],
        //   }));
        // setDiagram(newDiagram);
      } catch (err) {
        console.log("news제목 요약 불러오기 에러");
      }
    };
    fetchGetNews();
  }, [confirm]);

  const handleNewsClick = (value) => {
    setTitleId(value);
    console.log("selected title: ", title[value]);
  };

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
            height: "83vh",
            display: "flex",
            flexDirection: "column",
            p: 3,
            pt: 4,
            borderRight: { md: "1px solid lightgray" },
          }}
        >
          {/* 오늘 뉴스 */}
          <TopNews
            cnt={cnt}
            topicId={topicId}
            topicSummary={topicSummary}
            topicTitleSummary={topicTitleSummary}
            title={title}
            sentiment={sentiment}
            chooseNews={handleNewsClick}
          />

          {/* 다이어그램 */}
          <KeywordChart
            cnt={cnt}
            topicId={topicId}
            topicSummary={topicSummary}
            topicTitleSummary={topicTitleSummary}
            title={title}
            sentiment={sentiment}
            confirm={confirm}
          />
        </Grid>

        {/* 본문 우측 */}
        <Grid
          item
          sx={{
            width: { sm: "100%", md: "50%" },
            p: 3,
          }}
        >
          <NewsDetail
            titleId={titleId}
            topicId={topicId}
            topicSummary={topicSummary}
            title={title}
            confirm={confirm}
            chooseNews={handleNewsClick}
          />
        </Grid>
      </Grid>
    </>
  );
}
export default Allnews;
