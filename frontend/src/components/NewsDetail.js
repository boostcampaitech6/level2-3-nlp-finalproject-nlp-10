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
  Button,
  CardMedia,
} from "@mui/material";
import { SlArrowLeft, SlArrowRight } from "react-icons/sl";
import { GoSquareFill } from "react-icons/go";
import { MdFormatQuote } from "react-icons/md";
import { IconContext } from "react-icons";
import samsung from "../img/samsung.png";
import titleBackground from "../img/titleBackground.png"

export default function KeywordDetail(props) {
  let tags = ["언급량 1위", "매우 긍정적", "TV", "OLED"];
  const pageNum = [0, 1, 2, 3, 4];

  return (
    <>
      <Box height={"100%"}>
        <Box height={"92%"}>
          {/* <Box sx={{ p: 1.5, position: "relative" }}>
            <Box
              component="img"
              src={titleBackground}
              sx={{ objectFit: "cover", width: "100%", height: "100%" }}
            />
            <Box sx={{ fontFamily: "GmarketSansMedium", fontWeight: "bold", textAlign: "center", position: 'absolute', top: 30, justifyContent: 'center', alignItems: 'center', width: "90%" }}>
              <Typography sx={{ fontFamily: "GmarketSansMedium", fontWeight: "bold", textAlign: "center", position: 'relative', justifyContent: 'center', alignItems: 'center' }}>
                " {props.title[props.titleId]} "
              </Typography>
            </Box>
          </Box> */}
          <Box sx={{ p: 1.5, position: "relative" }}>
            <CardMedia
              component="img"
              src={titleBackground}
              sx={{ objectFit: "cover", width: "100%", height: "100%" }}
            />
            <Box sx={{
              position: 'absolute',
              fontFamily: "GmarketSansMedium",
              fontWeight: "bold",
              width: "90%",
              top: "50%",
              bottom: 0,
              left: "50%",
              transform: "translate(-50%, -25%)",
            }}
            >
              <Typography sx={{ fontFamily: "GmarketSansMedium", fontWeight: "bold", textAlign: "center", position: 'relative', }}>

                <MdFormatQuote style={{ transform: 'rotate(180deg)' }} /> {props.title[props.titleId]} <MdFormatQuote />
              </Typography>
            </Box>
          </Box>
          <Grid sx={{ display: "flex", flexDirection: "row", alignContent: "space-around", alignItems: 'center' }}>
            <Button onClick={() => { (props.titleId > 0) ? props.chooseNews(props.titleId - 1) : props.chooseNews(props.titleId) }} >
              <IconContext.Provider value={{ size: "40px" }}>
                <SlArrowLeft color="lightgray" />
              </IconContext.Provider>
            </Button>
            <Box sx={{ minHeight: "200px", width: "80%", margin: "auto", display: "block", padding: 3, }}>
              {/* 요약 뉴스 이미지 */}
              <Box
                component="img"
                src={samsung}
                sx={{ objectFit: "cover", width: "100%", height: "100%", }}
              />
            </Box>
            <Button onClick={() => { (props.titleId < 4) ? props.chooseNews(props.titleId + 1) : props.chooseNews(props.titleId) }} >
              <IconContext.Provider value={{ size: "40px" }}>
                <SlArrowRight color="lightgray" />
              </IconContext.Provider>
            </Button>
          </Grid>
          {/* 키워드 */}
          <Grid container>
            {tags.map((tag, idx) => (
              <Box key={idx} sx={{ pr: 2 }}>
                <Chip label={`# ${tag}`}
                  variant='outlined'
                  size='small'
                  sx={{
                    fontFamily: "GmarketSansMedium",
                    textAlign: "center",
                    fontSize: "0.7rem",
                    bgcolor: "#f2f7fb",
                    borderColor: "#e0e2e4",
                    borderWidth: "1.5px"
                  }}
                />
              </Box>
            ))}
          </Grid>
          {/* 뉴스 요약 */}
          <List sx={{ pl: 2.5, listStyleType: 'square' }}>
            <ListItem sx={{ display: 'list-item', p: 1, fontSize: "1rem", fontFamily: "Noto Sans KR" }}                  >
              {props.topicSummary[props.titleId]}
            </ListItem>
          </List>
        </Box>
        <Box display="flex" justifyContent="center" p={1}>
          <Grid sx={{ width: "30%", display: "flex", justifyContent: "space-around" }}>
            {props.title.slice(0, 5).map((title, idx) => (
              <GoSquareFill style={{ color: props.titleId == idx ? "#54cc99" : "lightgray" }} />
            ))}
          </Grid>
        </Box>
      </Box >
    </>
  )
}
