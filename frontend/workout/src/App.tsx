import { createBrowserRouter, RouterProvider } from "react-router";
import Home from "./pages/Home";
import Register from "./pages/Register";
import ProgramCreate from "./pages/ProgramCreate";
import Login from "./pages/Login";

function App() {
  const router = createBrowserRouter([
    {
      path: "/home",
      Component: Home,
    },
    {
      path: "/register",
      Component: Register,
    },
    {
      path: "/programs/create",
      Component: ProgramCreate,
    },
    {
      path: "/login",
      Component: Login,
    },
  ]);
  return (
    <div className="App ">
      <RouterProvider router={router} />
    </div>
  );
}

export default App;
