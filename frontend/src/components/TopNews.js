import { React, useEffect, useState } from "react";
import "../css/font.css";
import "../css/layout.css";
import { Box, Typography, List, ListItem } from "@mui/material";
import { IoLogoDesignernews } from "react-icons/io5";
import { IconContext } from "react-icons";
import {
  BsEmojiSmileFill,
  BsEmojiNeutralFill,
  BsEmojiFrownFill,
} from "react-icons/bs";
import { FaBrain } from "react-icons/fa";
import { TbArrowBadgeRightFilled } from "react-icons/tb";

export default function TopNews(props) {
  let date = "최신";
  return (
    <>
      <Box sx={{ display: "flex" }}>
        <IconContext.Provider value={{ size: "30px" }}>
          <TbArrowBadgeRightFilled color="#34b37d" />
        </IconContext.Provider>
        <Typography
          variant="h5"
          sx={{
            fontFamily: "GmarketSansMedium",
            fontWeight: "bold",
            pl: 1,
          }}
        >
          Top5 뉴스
        </Typography>
      </Box>

      {/* 뉴스 기사 제목 */}
      <List sx={{ p: 1, pl: 2.5, listStyleType: "square" }}>
        {props.title.slice(0, 5).map((it, idx) => (
          <ListItem
            key={idx}
            onClick={() => props.chooseNews(idx)}
            sx={{
              display: "list-item",
              p: 0.5,
              fontFamily: "Noto Sans KR",
              "&:hover": { fontWeight: "bold" },
            }}
          >
            {it}{" "}
            {idx % 2 == 0 ? (
              <BsEmojiSmileFill color="#5dc2b1" />
            ) : (
              <BsEmojiFrownFill color="#ed9568" />
            )}
          </ListItem>
        ))}
      </List>
    </>
  );
}
