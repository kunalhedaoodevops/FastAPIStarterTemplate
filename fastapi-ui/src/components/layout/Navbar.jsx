export default function Navbar() {
  return (
    <header className="h-16 bg-white border-b flex items-center justify-between px-6">
      <span className="font-semibold"></span>

      <button
        onClick={() => {
          localStorage.removeItem("access_token");
          window.location.href = "/login";
        }}
        className="bg-black text-white px-4 py-2 rounded"
      >
        Logout
      </button>
    </header>
  );
}
