import React, { useEffect, useRef, useState } from "react";
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
  Divider,
  List,
  ListItem,
} from "@mui/material";
import * as d3 from "d3";
import "../css/style.css";

// const data = [
//   {
//     label: "welcome",
//     value: 5,
//     color: "rgb(255, 69, 96)",
//   },
//   {
//     label: "activation",
//     value: 8,
//     color: "rgb(255, 69, 96)",
//   },
//   {
//     label: "use casesbusiness painpoints",
//     value: 8,
//     color: "rgb(255, 69, 96)",
//   },
//   {
//     label: "discuss openly",
//     value: 9,
//     color: "rgb(255, 69, 96)",
//   },
//   {
//     label: "heavy liftAgenda",
//     value: 7,
//     color: "rgb(255, 69, 96)",
//   },
//   {
//     label: "Scorecards",
//     value: 10,
//     color: "rgb(255, 69, 96)",
//   },
// ];

const Bub = ({
  cnt,
  topicId,
  topicSummary,
  topicTitleSummary,
  title,
  diagram,
  confirm,
}) => {
  const [data, setData] = useState([
    {
      label: "SET FILTER",
      value: 2,
      color: "#4EBF9A",
    },
  ]);

  const containerRef = useRef(null);
  const [hoveredNode, setHoveredNode] = useState(null);

  const handleMouseEnter = (event, d) => {
    setHoveredNode(d);
  };

  const handleMouseLeave = () => {
    setHoveredNode(null);
  };

  useEffect(() => {
    setData(diagram);
  }, [diagram]);

  useEffect(() => {
    // setData(diagram);
    const handleResize = () => {
      d3.select(containerRef.current).selectAll("*").remove();
      const containerWidth = containerRef.current.offsetWidth;
      const containerHeight = containerRef.current.offsetHeight;

      const chartContainer = d3.select(containerRef.current);
      chartContainer.select("svg").remove();

      const svg = chartContainer
        .append("svg")
        .attr("width", containerWidth)
        .attr("height", containerHeight);

      // Rest of your code...
      // ...
      const padding = 20;
      const diameter = Math.min(containerWidth, containerHeight) - padding;
      const format = d3.format(",d");

      const bubble = d3.pack().size([diameter, diameter]).padding(1.5);

      const root = d3.hierarchy({ children: data }).sum((d) => d.value);

      bubble(root);

      const nodes = d3
        .select(svg.node())
        .append("g")
        .attr("class", "gcontainer")
        .selectAll(".node")
        .data(root.children)
        .enter()
        .append("g")
        .attr("class", "node")
        .attr("transform", (d) => `translate(${d.x},${d.y})`)
        .on("mouseenter", handleMouseEnter)
        .on("mouseleave", handleMouseLeave);

      const circles = nodes
        .append("circle")
        .attr("r", 0)
        .style("fill", (d) => d.data.color);

      circles
        .transition()
        .duration(1000)
        .attr("r", (d) => d.r);

      const text = nodes
        .append("text")
        .style(
          "font-size",
          (d) =>
            Math.min(10 * d.r, (10 * d.r - 8) / d.data.label.length / 2) + "px"
        )
        .attr("dy", ".3em")
        .style("text-anchor", "middle")
        .style("font-weight", "bold")
        .style("color", "white")
        .style("font-style", "Georgia")
        .style("opacity", 0)
        // .text((d) => d.data.label);
        .text((d) => d.data.label.slice(0, d.data.label.length / 2));

      // const text = nodes
      //   .append("text")
      //   .style(
      //     "font-size",
      //     (d) =>
      //       Math.min(6.5 * d.r, (6.5 * d.r - 8) / d.data.label.length / 2) +
      //       "px"
      //   )
      //   .attr("dy", ".3em")
      //   .style("text-anchor", "middle")
      //   .style("font-weight", "bold")
      //   .style("opacity", 0)
      //   .selectAll("tspan")
      //   .data((d) => {
      //     const label = d.data.label;
      //     return [
      //       label.slice(0, Math.ceil(label.length / 2)),
      //       label.slice(Math.ceil(label.length / 2)),
      //     ];
      //   })
      //   .enter()
      //   .append("tspan")
      //   .attr("x", 0)
      //   .attr("dy", (d, i, nodes) => (i === 0 ? "0em" : "1.1em")) // 첫 줄은 0em, 그 이후부터는 1.1em
      //   .text((d) => d);

      text.transition().duration(1000).style("opacity", 1);

      console.log(
        d3
          .select(containerRef.current)
          .selectAll("g")
          .node()
          .getClientRects()[0].height
      );
      var element = d3.select(".gcontainer").node();
      console.log(element);
      var gWidth = d3
        .select(containerRef.current)
        .selectAll("g")
        .node()
        .getClientRects()[0].width;
      var gHeight = d3
        .select(containerRef.current)
        .selectAll("g")
        .node()
        .getClientRects()[0].height;
      //   console.log({ gWidth, gHeight });

      const x = (containerWidth - gWidth) / 2.5;
      const y = (containerHeight - gHeight) / 50;

      d3.select(".gcontainer").attr("transform", `translate(${x}, ${y})`);
    };

    handleResize();

    window.addEventListener("resize", handleResize);

    return () => {
      window.removeEventListener("resize", handleResize);
    };
  }, [confirm]);

  const Tooltip = () => {
    const [tooltipPosition, setTooltipPosition] = useState({ x: 0, y: 0 });

    const handleMouseMove = (event) => {
      const { clientX, clientY } = event;
      setTooltipPosition({ x: clientX, y: clientY + 300 });
    };

    useEffect(() => {
      document.addEventListener("mousemove", handleMouseMove);

      return () => {
        document.removeEventListener("mousemove", handleMouseMove);
      };
    }, []);

    if (!hoveredNode) {
      return null;
    }

    const { label, label2, value, color } = hoveredNode.data;
    // console.log(hoveredNode);
    return (
      <div
        className="tooltip"
        style={{
          left: tooltipPosition.x,
          top: tooltipPosition.y,
          background: color,
        }}
      >
        <div>{label2}</div>
        <div>{value}개의 관련 기사</div>
      </div>
    );
  };

  return (
    <Box>
      <div className="bubble-chart-container">
        <div ref={containerRef} style={{ height: "39vh", width: "44vw" }} />
        <Tooltip />
      </div>
    </Box>
  );
};

export default Bub;
