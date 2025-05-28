import { NavLink, useNavigate } from "react-router";
import { useMutation, useQuery } from "@tanstack/react-query";
import { getUserProfile } from "../api/apiFns";
import api from "../api/axios";

const Navbar = () => {
  const navigate = useNavigate();
  const { data: user, isLoading } = useQuery({
    queryKey: ["userProfile"],
    queryFn: getUserProfile,
    retry: false,
    refetchOnWindowFocus: false,
  });
  const logoutMutation = useMutation({
    mutationFn: () => api.post("/logout/"),
    onSuccess: () => {
      navigate("/login", { replace: true });
    },
  });

  return (
    <nav className="bg-white text-black font-bold text-lg shadow-md w-full relative flex items-center">
      <div className="flex items-center justify-between w-full px-6 py-4">
        <div className="space-x-4">
          <NavLink to="/home" className="hover:underline">
            Home
          </NavLink>

          {!isLoading && user ? (
            <>
              <NavLink to="/myprograms" className="hover:underline">
                Programs
              </NavLink>
              <NavLink to="/myprofile" className="hover:underline">
                Profile
              </NavLink>
              <NavLink to="/coaches" className="hover:underline">
                Coaches
              </NavLink>
              <NavLink to="/payments" className="hover:underline">
                My payments
              </NavLink>
              <button
                className="hover:underline"
                onClick={() => logoutMutation.mutate()}
              >
                Logout
              </button>
            </>
          ) : (
            <>
              <NavLink to="/login" className="hover:underline">
                Login
              </NavLink>
              <NavLink to="/register" className="hover:underline">
                Register
              </NavLink>
            </>
          )}
        </div>
      </div>
    </nav>
  );
};


export default Navbar;
