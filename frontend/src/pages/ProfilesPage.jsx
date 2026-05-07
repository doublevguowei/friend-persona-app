import { Link } from "react-router-dom";

import { useUsers } from "../hooks";
import LoadingState from "../shared/LoadingState.jsx";
import Message from "../shared/Message.jsx";

export default function ProfilesPage() {
  const { data: users, error, loading } = useUsers();

  return (
    <section className="stack-page">
      <div className="page-title-row">
        <div>
          <span className="eyebrow">人格档案</span>
          <h1>选择一个群友开盒</h1>
        </div>
      </div>

      {loading && <LoadingState text="正在搬出档案柜..." />}
      {error && <Message tone="error">{error}</Message>}

      <div className="profile-grid">
        {users?.map((user) => (
          <Link key={user.id} className="profile-card-link" to={`/profile/${user.id}`}>
            <span className="avatar">{user.avatar}</span>
            <strong>{user.nickname}</strong>
            <small>查看人格数值</small>
          </Link>
        ))}
      </div>
    </section>
  );
}
