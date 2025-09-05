import Navbar from "./Navbar";
import { Outlet } from "react-router-dom";

export default function Layout({hideNavbar = false}) {
  return (
    <div className="page-container">
      {!hideNavbar && <Navbar />}
      <div className="cont-container">
        <Outlet />
      </div>
    </div>
  );
}