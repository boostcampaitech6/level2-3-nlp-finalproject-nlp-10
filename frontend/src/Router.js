import { BrowserRouter, Routes, Route } from "react-router-dom";
import Contents from "./pages/Contents";
import Main from "./pages/Main";
import BubbleCrt from "./components/Bubble";
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
        </>
      </Routes>
    </BrowserRouter>
  );
}

export default Router;
