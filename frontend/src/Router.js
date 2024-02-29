import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import Allnews from './pages/Allnews';

function Router() {
  return (
    <BrowserRouter>
      <Routes>
        <>
          <Route path="/" element={<Allnews />} />
        </>
      </Routes>
    </BrowserRouter>
  );
}

export default Router;