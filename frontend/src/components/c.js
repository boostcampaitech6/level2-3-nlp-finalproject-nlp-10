const bubbleData = [
  {
    fillColor: "rgb(52, 202, 173, 0.3)",
    id: 5,
    name: "Setting\nme",
    size: 50,
    dYdX1: { dy: -2, dx: -3 },
    dYdX2: { dy: 8, dx: -20 },
  },
  {
    fillColor: "rgb(52, 202, 173, 0.3)",
    id: 6,
    name: "Getting\nStart",
    size: 120,
    dYdX1: { dy: -2, dx: -4 },
  },
  {
    fillColor: "rgb(52, 202, 173, 0.3)",
    id: 7,
    name: "Setting\nme",
    size: 50,
    dYdX1: { dy: -2, dx: -3 },
    dYdX2: { dy: 8, dx: -20 },
  },
];

const [diagram, setDiagram] = useState([]);
const newDiagram = topicTitleSummary.map((title, index) => ({
  name: title,
  size: cnt[index],
  fillColor: "rgb(52, 202, 173, 0.3)",
  id: { index },
  dYdX1: { dy: -2, dx: -3 },
  dYdX2: { dy: 8, dx: -20 },
}));
setDiagram(newDiagram);
