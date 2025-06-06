import { createBrowserRouter, RouterProvider } from "react-router";
import {QueryClientProvider} from "@tanstack/react-query"
import Home from "./pages/Home";
import Register from "./pages/Register";
import ProgramCreate from "./pages/ProgramCreate";
import Login from "./pages/Login";
import Programs from "./pages/Programs";
import User from "./pages/User";
import Layout from "./components/Layout";
import Coaches from "./pages/Coaches";
import Subscription from "./pages/Subscription";
import Payments from "./pages/Payments";
import AdvertiserLogin from "./pages/AdvertiserLogin";
import { queryClient } from "./queryClient";
import { userLoader } from "./loaders/userLoader";

function App() {

  const router = createBrowserRouter([
    {
      Component: Layout,
      children: [
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
        {
          path: "/myprograms",
          Component: Programs,
        },
        {
          path: "/myprofile",
          Component: User,
          loader: userLoader,
        },
        {
          path: "/coaches",
          Component: Coaches,
        },
        {
          path: "/change-subscription",
          Component: Subscription
        },
        {
          path: "/payments",
          Component: Payments
        },
        {
          path: "/advertiser/login",
          Component: AdvertiserLogin
        }
      ],
    },
  ]);
  return (
    <div className="App ">
      <QueryClientProvider client={queryClient}>
      <RouterProvider router={router} />
      </QueryClientProvider>
    </div>
  );
}

export default App;
