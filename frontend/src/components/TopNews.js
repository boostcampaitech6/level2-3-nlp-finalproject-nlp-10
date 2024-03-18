import { React, useEffect, useState } from "react";
import "../css/font.css";
import "../css/layout.css";
import { Box, Typography, List, ListItem } from "@mui/material";
import { IoLogoDesignernews } from "react-icons/io5";
import { IconContext } from "react-icons";

export default function TopNews(props) {
  let date = "최신";
  return (
    <>
      <Box sx={{ display: "flex" }}>
        <IconContext.Provider value={{ size: "25px" }}>
          <IoLogoDesignernews />
        </IconContext.Provider>
        <Typography
          variant="h5"
          sx={{
            fontFamily: "KOTRAHOPE",
            fontWeight: "normal",
            pl: 1.3,
          }}
        >
          뉴스 Top5
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
              fontSize: "1.5rem",
              fontFamily: "omyu_pretty",
              "&:hover": { fontWeight: "bold" }
            }}
          >
            {it}
          </ListItem>
        ))}
      </List>
    </>
  );
}
