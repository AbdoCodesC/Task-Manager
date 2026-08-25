import { useNavigate } from "react-router";

function Home() {
  const navigate = useNavigate();
  return (
    <div>
      <div>
        <h1>Hello, welcome to my App</h1>
        <button className="underline hover:text-blue-200 cursor-pointer" onClick={() => navigate("/login")}>
          Login
        </button>
      </div>
    </div>
  );
}

export default Home;
