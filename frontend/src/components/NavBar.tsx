import { logout } from "../utils/axios";
import { useNavigate } from "react-router";

function NavBar() {
  const navigate = useNavigate();
  return (
    <nav className="relative bg-gray-300 h-10">
      <div className="mx-auto px-2 sm:px-6 lg:px-8">
        <div className="flex flex-1 items-center justify-center sm:justify-start sm:items-stretch">
          <div className="flex space-x-4 self-center">
            <a className="p-2" href="/task">
              Tasks
            </a>
            <a className="p-2" href="/create-task">
              Create
            </a>
            <a className="p-2" href="/task">
              History
            </a>
          </div>
        </div>
        <div className="absolute right-2 top-1">
          <button
            type="button"
            onClick={() => {
              console.log("logging out");
              navigate("/home");
              return logout();
            }}
          >
            <svg
              width="30"
              height="30"
              viewBox="0 0 118 118"
              fill="none"
              xmlns="http://www.w3.org/2000/svg"
            >
              <path
                d="M108.167 59C108.167 86.1538 86.1537 108.167 58.9999 108.167C31.8459 108.167 9.83325 86.1538 9.83325 59C9.83325 31.846 31.8459 9.83333 58.9999 9.83333C86.1537 9.83333 108.167 31.846 108.167 59Z"
                stroke="#163300"
                strokeWidth="8.5"
              />
              <path
                d="M72.5209 46.7083C72.5209 54.1758 66.4675 60.2292 59.0001 60.2292C51.5326 60.2292 45.4792 54.1758 45.4792 46.7083C45.4792 39.241 51.5326 33.1875 59.0001 33.1875C66.4675 33.1875 72.5209 39.241 72.5209 46.7083Z"
                stroke="#163300"
                strokeWidth="8.5"
              />
              <path
                d="M27.0417 93.4172L29.797 88.5954C34.1739 80.9362 42.3195 76.2088 51.1416 76.2088H66.8587C75.6807 76.2088 83.8261 80.9362 88.2029 88.5954L90.9582 93.4172"
                stroke="#163300"
                strokeWidth="8.5"
                strokeLinecap="round"
                strokeLinejoin="round"
              />
            </svg>
          </button>
        </div>
      </div>
    </nav>
  );
}

export default NavBar;
