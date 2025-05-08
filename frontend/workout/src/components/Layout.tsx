import { Outlet } from "react-router";
import Navbar from "./Navbar";
import Footer from "./Footer";
import RightPanel from "./Ads/RightPanel";

const Layout = () => {
  return (
    <div className="min-h-screen text-center flex flex-col bg-neutral-200">
      <header>
        <Navbar />
      </header>

      {/* Main content and ads side by side */}
      <div className="flex flex-1">
        <main className="flex-1 p-4 overflow-auto">
          <Outlet />
        </main>
        <RightPanel />
      </div>

      <Footer />
    </div>
  );
};

export default Layout;
