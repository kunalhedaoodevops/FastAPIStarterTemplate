import { NavLink } from "react-router-dom";
import logo from "../../assets/logo.png";

const menu = [
  { name: "Dashboard", path: "/" },
  { name: "Users", path: "/users" },
  { name: "Items", path: "/items" },
  { name: "Files", path: "/files" },
  { name: "Health", path: "/health" },
];

export default function Sidebar() {
  return (
    <aside className="w-64 bg-white border-r h-screen">
      {/*<div className="p-5 text-xl font-bold">🚀 StarterTemplate</div>*/}
        <div className="flex items-center gap-3 p-5 text-xl font-bold">
  <img
    src={logo}
    alt="FastAPI Logo"
    className="w-6 h-6"
  />
  <span>StarterTemplate</span>
</div>


      <nav className="p-3 space-y-2">
        {menu.map((m) => (
          <NavLink
            key={m.path}
            to={m.path}
            className={({ isActive }) =>
              `block px-4 py-2 rounded ${
                isActive
                  ? "bg-black text-white"
                  : "hover:bg-gray-100"
              }`
            }
          >
            {m.name}
          </NavLink>
        ))}
      </nav>
    </aside>
  );
}
