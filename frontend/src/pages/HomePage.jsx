import { ArrowRight, Sparkles } from "lucide-react";
import { useNavigate } from "react-router-dom";

import { rememberUser, useUsers } from "../hooks";
import LoadingState from "../shared/LoadingState.jsx";
import Message from "../shared/Message.jsx";

export default function HomePage() {
  const navigate = useNavigate();
  const { data: users, error, loading } = useUsers();

  function chooseUser(user) {
    rememberUser(user.id);
    navigate(`/vote?user_id=${user.id}`);
  }

  return (
    <section className="home-page">
      <div className="hero-band">
        <div className="hero-kicker">
          <Sparkles size={16} />
          每日群友观察报告
        </div>
        <h1>群友人格档案馆</h1>
        <p>一个认真但不正经的群友人格记录系统</p>
      </div>

      <div className="section-heading">
        <h2>选择今天的身份</h2>
        <span>6 人限定内测版</span>
      </div>

      {loading && <LoadingState text="正在召集群友..." />}
      {error && <Message tone="error">{error}</Message>}

      <div className="identity-grid">
        {users?.map((user) => (
          <button key={user.id} className="identity-card" onClick={() => chooseUser(user)}>
            <span className="avatar" aria-hidden="true">
              {user.avatar}
            </span>
            <span className="identity-main">
              <strong>{user.nickname}</strong>
              <small>进入今日投票</small>
            </span>
            <ArrowRight size={18} />
          </button>
        ))}
      </div>
    </section>
  );
}
