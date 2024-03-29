import React from "react";
import { useState, useEffect, useRef } from "react";
import "../css/font.css";
import "../css/layout.css";
import { Grid, Button } from "@mui/material";
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
  const [companyInfo, setCompanyInfo] = useState({});
  const [positiveNum, setPositiveNum] = useState();
  const [neutralNum, setNeutralNum] = useState();
  const [negativeNum, setNegativeNum] = useState();
  const [closePriceInfo, setClosePriceInfo] = useState([]);

  const divRef = useRef(null);

  const scrollToTop = () => {
    divRef.current.scroll({
      top: 0,
      behavior: "smooth",
    });
  };

  const [sentimentCounts, setSentimentCounts] = useState({});
  const [sentimentNews, setSentimentNews] = useState({
    0: [],
    1: [],
    2: [],
  });
  useEffect(() => {
    function countSentiments(objects) {
      const counts = {};
      objects.forEach((obj) => {
        const sentiment = obj.sentiment;
        counts[sentiment] = (counts[sentiment] || 0) + 1;
      });
      return counts;
    }
    function compare(a, b) {
      if (a.cnt < b.cnt) {
        return -1;
      }
      if (a.cnt > b.cnt) {
        return 1;
      }
      return 0;
    }
    function classifyBySentiment(data) {
      const lis = {
        0: [],
        1: [],
        2: [],
      };

      data.sort(compare);

      data.forEach((obj) => {
        const { sentiment, news_title } = obj;
        if (obj.sentiment in [0, 1, 2]) {
          lis[obj.sentiment].push(obj.news_title);
        }
      });

      return lis;
    }

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
        setSentimentCounts(countSentiments(response.data));
        console.log("sentimentCounts", sentimentCounts);

        setSentimentNews(classifyBySentiment(response.data));
        console.log("SentimentNews", sentimentNews);

        console.log("최신 뉴스 불러오기", response.data);
        setCnt(response.data.map((item) => item.cnt));
        setNewsId(response.data.map((item) => item.news_id));
        setNewsTitle(response.data.map((item) => item.news_title));
        setSummary(response.data.map((item) => item.summary));
        setSentiment(response.data.map((item) => item.sentiment));
        setPositiveNum(response.data.filter((item) => item.sentiment === 2).length);
        setNeutralNum(response.data.filter((item) => item.sentiment === 1).length);
        setNegativeNum(response.data.filter((item) => item.sentiment === 0).length);
      } catch (err) {
        console.log("최신 뉴스 불러오기 에러");
        console.log("최신 뉴스 불러오기 에러");
      }
    };

    const fetchCompanyInfo = async () => {
      try {
        const response = await axios.get(
          "http://localhost:8000/jh/get-company-info",
          {
            params: {
              company_id: company ? company : company_id,
            },
          }
        );
        console.log("company info: ", response.data);
        setCompanyInfo(response.data);
      } catch (err) {
        console.log("company info fetch error");
      }
    };

    const fetchCompanyClosePrice = async () => {
      try {
        const response = await axios.get("http://localhost:8000/jh/get-company-close-price-90",
          {
            params: {
              company_id: company ? company : company_id,
            }
          }
        )
        console.log("company close price: ", response.data)
        setClosePriceInfo(response.data)
      } catch (err) {
        console.log("company close price fetch error")
      }
    }

    fetchGetNews();
    fetchCompanyInfo();
    fetchCompanyClosePrice();
    setCompanyId(company);
    scrollToTop();
  }, [confirm]);

  const [isBottom, setIsBottom] = useState(false);
  const [isTop, setIsTop] = useState(true);

  const handleScroll = (e) => {
    if (
      Math.abs(
        e.target.scrollHeight - e.target.clientHeight - e.target.scrollTop
      ) <= 1
    ) {
      setIsBottom(true);
      setIsTop(false);
    } else if (e.currentTarget.scrollTop === 0) {
      setIsTop(true);
      setIsBottom(false);
    }
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
            display: "flex",
            flexDirection: "column",
            p: 4,
            borderRight: { md: "1px solid lightgray" },
          }}
        >
          <Grid
            onScroll={handleScroll}
            ref={divRef}
            sx={{
              height: "72vh",
              overflowY: "scroll",
              "&-ms-overflow-style": "none",
              "&::-webkit-scrollbar": { display: "none" },
            }}
          >
            <CompanyRecentNews
              cnt={cnt}
              newsId={newsId}
              newsTitle={newsTitle}
              summary={summary}
              sentiment={sentiment}
            />
          </Grid>
          <Grid
            sx={{
              height: "3vh",
              display: "flex",
              justifyContent: "center",
              pt: 2,
            }}
          >
            {isBottom && (
              <Button onClick={() => scrollToTop()}>
                <RxDoubleArrowUp color="#a1a1a1" fontSize={"1.3rem"} />
              </Button>
            )}
            {isTop && <RxDoubleArrowDown color="#a1a1a1" fontSize={"1.3rem"} />}
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
          <Grid >
            <StockInfo
              closePriceInfo={closePriceInfo}
              companyInfo={companyInfo}
              companyId={companyId}
            />
          </Grid>
          <Grid>
            <SentimentInfo
              companyId={companyId}
              positiveNum={positiveNum}
              neutralNum={neutralNum}
              negativeNum={negativeNum}
              sentimentCounts={sentimentCounts}
              sentimentNews={sentimentNews}
            />
          </Grid>
        </Grid>
      </Grid>
    </>
  );
}
export default CompanyInfo;
