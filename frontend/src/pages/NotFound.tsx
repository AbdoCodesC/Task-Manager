function NotFound() {
  return (
    <div className="flex w-full justify-between h-screen overflow-hidden border">
      <div className="flex flex-col gap-5 justify-around">
        <div className="flex w-full">
          {/* left */}
          <div className="flex px-10 justify-center items-center flex-1">
            <img src="/404.svg" alt="" className="w-full" />
          </div>
          {/* right */}
          <div className="flex flex-1 items-center justify-start">
            <div className="flex flex-col gap-10">
              <p className="text-9xl text-blue-900 font-bold">404</p>
              <p className="text-5xl font-bold">Page Not Found</p>
              <p className="text-lg text-gray-400 font-bold">
                The page you're looking for doesn't exist or has been moved.
              </p>
            </div>
          </div>
        </div>
        <div className="flex w-full justify-center items-center">
          <a href="/">
            <button className="flex justify-center py-2 px-3 items-center bg-blue-600 hover:bg-blue-800 cursor-pointer rounded-lg text-white">
              Go Back Home
            </button>
          </a>
        </div>
      </div>
    </div>
  );
}

export default NotFound;
