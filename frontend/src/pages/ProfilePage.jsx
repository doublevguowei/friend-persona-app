import { Link, useParams } from "react-router-dom";

import { apiFetch } from "../api";
import { useAsyncData } from "../hooks";
import LoadingState from "../shared/LoadingState.jsx";
import Message from "../shared/Message.jsx";
import { traitLabels } from "../traits";

export default function ProfilePage() {
  const { userId } = useParams();
  const { data, error, loading } = useAsyncData(() => apiFetch(`/profile/${userId}`), [userId]);

  const scores = data?.user.scores || {};
  const maxScore = Math.max(6, ...Object.values(scores));

  return (
    <section className="stack-page">
      {loading && <LoadingState text="正在翻档案..." />}
      {error && <Message tone="error">{error}</Message>}

      {data && (
        <>
          <div className="profile-hero">
            <span className="profile-avatar">{data.user.avatar}</span>
            <div>
              <span className="eyebrow">人格档案</span>
              <h1>{data.user.nickname}</h1>
              <p>今日被点名 {data.today_received_votes} 次，历史累计 {data.total_received_votes} 次</p>
            </div>
          </div>

          <div className="score-panel">
            {Object.entries(traitLabels).map(([key, label]) => {
              const value = scores[key] || 0;
              return (
                <div key={key} className="score-row">
                  <div className="score-label">
                    <span>{label}</span>
                    <strong>{value}</strong>
                  </div>
                  <div className="score-track">
                    <span style={{ width: `${Math.max(6, (value / maxScore) * 100)}%` }} />
                  </div>
                </div>
              );
            })}
          </div>

          <div className="titles-panel">
            <div className="section-heading compact">
              <h2>最近获得的称号</h2>
              <Link to="/profiles">切换档案</Link>
            </div>
            {data.recent_titles.length === 0 ? (
              <Message>暂时还没有称号，今天很适合刷一波存在感。</Message>
            ) : (
              <div className="title-list">
                {data.recent_titles.map((item) => (
                  <div key={`${item.date}-${item.question}`} className="title-item">
                    <strong>{item.title}</strong>
                    <span>
                      {item.date} · {item.votes} 票
                    </span>
                  </div>
                ))}
              </div>
            )}
          </div>
        </>
      )}
    </section>
  );
}
