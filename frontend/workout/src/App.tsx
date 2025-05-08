import { createBrowserRouter, RouterProvider } from "react-router";
import {QueryClient, QueryClientProvider} from "@tanstack/react-query"
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

function App() {
  const queryClient = new QueryClient();

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
