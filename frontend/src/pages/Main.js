import React from 'react'
import { useState } from "react";
import "../css/font.css";
import "../css/layout.css";
import {
  Box,
  createTheme,
  Grid,
  Container,
  Typography,
  Paper,
  InputLabel,
  MenuItem,
  FormControl,
  Select,
  Button,
  ButtonGroup,
} from "@mui/material";
import NavBar from "../components/NavBar"
import CompanyInfo from './CompanyInfo';
import Companynews from './Companynews';
import Allnews from './Allnews';
import { IoLogoDesignernews } from "react-icons/io5";
import { IconContext } from "react-icons";
import { FaBackward } from "react-icons/fa6";
import { VscSymbolKeyword } from "react-icons/vsc";

import diagram from "../img/diagram.png";
import samsung from "../img/samsung.png";

const styles = (theme) => ({
  root: {
    // padding: theme.spacing(3),
    margin: 0,
    padding: 0,
    background: "#eeeee",
  },
  paper: {
    padding: theme.spacing(3),
    color: theme.pallete.text.primary,
  },
  box: {
    padding: theme.spacing(5),
    color: theme.pallete.text.warn,
  },
});

export default function Main() {
  const [value, setValue] = useState("0");

  const handleChange = (e, newValue) => {
    setValue(newValue)
  }

  return (
    <>
      <div className={styles.root} name="main">
        <NavBar selectedTab={value} onClickTab={handleChange} />
        {value == "0" && <Allnews />}
        {value == "1" && <CompanyInfo />}
      </div>
    </>
  )
}
