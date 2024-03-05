import { BrowserRouter, Routes, Route } from "react-router-dom";
import Companynews from "./pages/Companynews";
import Allnews from "./pages/Allnews";

function Router() {
  return (
    <BrowserRouter>
      <Routes>
        <>
          <Route path="/company" element={<Companynews />} />
          <Route path="/" element={<Allnews />} />
        </>
      </Routes>
    </BrowserRouter>
  );
}

export default Router;
