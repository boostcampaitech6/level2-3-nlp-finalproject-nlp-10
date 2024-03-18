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
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faChevronLeft, faChevronRight, faSquare } from '@fortawesome/free-solid-svg-icons'
import samsung from "../img/samsung.png";

export default function KeywordDetail(props) {
  let tags = ["언급량 1위", "매우 긍정적", "TV", "OLED"];
  const pageNum = [0, 1, 2, 3, 4];

  return (
    <>
      <Box height={"100%"}>
        <Box height={"92%"}>
          <Box sx={{ p: 1.5, backgroundColor: "rgb(218, 248, 240)" }}>
            {/* 제목 */}
            <Typography sx={{ fontFamily: "KOTRAHOPE", textAlign: "center", }}>
              " {props.title[props.titleId]} "
            </Typography>
          </Box>
          <Grid sx={{ display: "flex", flexDirection: "row", alignContent: "space-around", alignItems: 'center' }}>
            <FontAwesomeIcon icon={faChevronLeft} size="3x" color="lightgray" onClick={() => { (props.titleId > 0) ? props.chooseNews(props.titleId - 1) : props.chooseNews(props.titleId) }} />
            <Box sx={{ minHeight: "200px", width: "80%", margin: "auto", display: "block", padding: 3, }}>
              {/* 요약 뉴스 이미지 */}
              <Box
                component="img"
                src={samsung}
                sx={{ objectFit: "cover", width: "100%", height: "100%", }}
              />
            </Box>
            <FontAwesomeIcon icon={faChevronRight} size="3x" color="lightgray" onClick={() => { (props.titleId < 4) ? props.chooseNews(props.titleId + 1) : props.chooseNews(props.titleId) }} />
          </Grid>
          {/* 키워드 */}
          <Grid container>
            {tags.map((tag, idx) => (
              <Box key={idx} sx={{ pr: 2 }}>
                <Chip label={`# ${tag}`}
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
            <ListItem sx={{ display: 'list-item', p: 1, fontSize: "1rem", fontFamily: "omyu_pretty" }}                  >
              {props.topicSummary[props.titleId]}
            </ListItem>
          </List>
        </Box>
        <Box display="flex" justifyContent="center" p={1}>
          <Grid sx={{ width: "30%", display: "flex", justifyContent: "space-around" }}>
            {pageNum.map((page, idx) => (
              <FontAwesomeIcon icon={faSquare} size="xs" style={{ color: props.titleId == page ? "#54cc99" : "lightgray" }} />
            ))}
          </Grid>
        </Box>
      </Box>
    </>
  )
}
