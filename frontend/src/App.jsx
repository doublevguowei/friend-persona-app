import { BookUser, ChartNoAxesColumnIncreasing, Home, Trophy, Vote } from "lucide-react";
import { NavLink, Outlet, useLocation } from "react-router-dom";

function getSelectedUserId() {
  return window.localStorage.getItem("friend_persona_user_id");
}

export default function AppShell() {
  const location = useLocation();
  const selectedUserId = getSelectedUserId();
  const votePath = selectedUserId ? `/vote?user_id=${selectedUserId}` : "/";

  const navItems = [
    { label: "首页", path: "/", icon: Home, end: true },
    { label: "投票", path: votePath, icon: Vote },
    { label: "今日结果", path: "/results", icon: Trophy },
    { label: "排行榜", path: "/leaderboard", icon: ChartNoAxesColumnIncreasing },
    { label: "人格档案", path: "/profiles", icon: BookUser }
  ];

  return (
    <div className="app-shell">
      <main className="page-wrap">
        <Outlet />
      </main>

      <nav className="bottom-nav" aria-label="底部导航">
        {navItems.map((item) => {
          const Icon = item.icon;
          const isProfileActive = item.path === "/profiles" && location.pathname.startsWith("/profile");
          return (
            <NavLink
              key={item.label}
              to={item.path}
              end={item.end}
              className={({ isActive }) => `nav-item ${isActive || isProfileActive ? "active" : ""}`}
            >
              <Icon size={20} strokeWidth={2.2} />
              <span>{item.label}</span>
            </NavLink>
          );
        })}
      </nav>
    </div>
  );
}
