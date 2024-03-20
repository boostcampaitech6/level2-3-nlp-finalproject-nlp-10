import { BrowserRouter, Routes, Route } from "react-router-dom";
import Contents from "./pages/Contents";
import Main from "./pages/Main";
import BubbleCrt from "./components/Bubble";
import Example from "./components/Example";
import Tree from "./components/Bub";
// import Companynews from "./pages/Companynews";
// import Allnews from "./pages/Allnews";

function Router() {
  return (
    <BrowserRouter>
      <Routes>
        <>
          <Route path="/" element={<Main />} />
          <Route path="/contents" element={<Contents />} />
          <Route path="/bubble" element={<BubbleCrt />} />
          <Route path="/example" element={<Example />} />
          <Route path="/tree" element={<Tree />} />
        </>
      </Routes>
    </BrowserRouter>
  );
}

export default Router;
