import { NavLink } from "react-router";

const Navbar = () => {
  return (
    <nav className="bg-white text-black font-bold text-lg shadow-md w-full relative flex items-center">
      <div className="flex items-center justify-between w-full px-6 py-4">
        <div className="space-x-4">
          <NavLink to={"/home"} className="hover:underline">
            Home
          </NavLink>
          <NavLink to={"/myprograms"} className="hover:underline">
            Programs
          </NavLink>
          <NavLink to={"/myprofile"} className="hover:underline">
            Profile
          </NavLink>
          <NavLink to={"/coaches"} className="hover:underline">
            Coaches
          </NavLink>
          <NavLink to={"/payments"} className="hover:underline">
            My payments
          </NavLink>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
