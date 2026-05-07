export default function Message({ children, tone = "info" }) {
  return <div className={`message ${tone}`}>{children}</div>;
}
