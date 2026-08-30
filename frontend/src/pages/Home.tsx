import {
  SquareCheckBig,
  Rocket,
  Play,
  Users,
  Bell,
  ChartNoAxesCombined,
  Mail,
} from "lucide-react";

import FeatureCard from "../components/cards/FeatureCard";

function Home() {
  return (
    <div className="h-full bg-white px-10">
      {/* Nav Bar */}
      <section>
        <div className="flex justify-between items-center w-full p-4 h-20">
          {/* Left */}
          <div className="flex">
            <SquareCheckBig color="#dbeafe" size={30} />
            <h1 className="ml-1 font-bold text-xl">TaskManager</h1>
          </div>
          {/* Middle */}
          <div className="flex gap-10 text-gray-500">
            <a
              href="#features"
              className="hover:underline transition-all delay-150 ease-in-out duration-300 hover:-translate-y-0.5 "
            >
              Features
            </a>
            <a
              href="#how"
              className="hover:underline transition-all delay-150 ease-in-out duration-300 hover:-translate-y-0.5 "
            >
              How it works
            </a>
            <a
              href="/about"
              className="hover:underline transition-all delay-150 ease-in-out duration-300 hover:-translate-y-0.5 "
            >
              About
            </a>
          </div>
          {/* End */}
          <div>
            <a
              href="/signup"
              className="p-4 bg-blue-400 rounded-lg text-gray-100 hover:bg-blue-300 cursor-pointer transition-colors ease-in-out delay-50 duration-200 hover:scale-100"
            >
              Get started
            </a>
          </div>
        </div>
      </section>
      {/* Hero */}
      <section>
        <div className="w-full h-full my-10 flex justify-around">
          {/* Left */}
          <div className="flex mt-5">
            <div className="">
              <div className="flex text-xs py-1 w-50 bg-blue-200 rounded-md text-blue-400 justify-center items-center mb-5">
                <Rocket size={12} />
                <p className="ml-1">Stay organized. Get more done.</p>
              </div>
              <div className="font-bold flex flex-col text-2xl">
                <h1>Organize Your Work.</h1>
                <h2 className="text-blue-400">Achieve More.</h2>
              </div>
              <div className="flex flex-wrap mt-4">
                <p className="text-sm text-gray-500">
                  Task manager helpes you plan you day, track progress, and
                  collaborate with your team — all in one place.
                </p>
              </div>
              <div className="flex mt-8">
                <a
                  href="/signup"
                  className="p-4 mt-5 bg-blue-400 rounded-lg text-gray-100 hover:bg-blue-300 cursor-pointer transition-colors ease-in-out delay-50 duration-200 "
                >
                  Get Started — It's Free
                </a>
                {/* <div className="flex"> */}
                <button
                  type="button"
                  className="p-4 mt-5 ml-5 bg-gray-500 rounded-lg text-gray-100 hover:bg-gray-300 cursor-pointer transition-colors ease-in-out delay-50 duration-200 flex justify-center items-center"
                >
                  <span className="mr-1">{<Play size={14} />}</span>
                  Watch Demo
                </button>
                {/* </div> */}
              </div>
            </div>
          </div>
          {/* Right */}
          <div className="flex flex-col">
            <div className="h-full w-full">
              <div className="w-full h-full">
                <img src="/tasks.svg" alt="" className="block w-full h-full" />
              </div>
              <img
                src="/progress.svg"
                alt=""
                className="-translate-x-32 -translate-y-25 w-50 h-30"
              />
            </div>
          </div>
        </div>
      </section>
      {/* Features */}
      <section>
        <div className="w-full h-full mt-15 mb-10">
          {/* Center */}
          <div className="flex flex-col">
            <div className="flex flex-col justify-center items-center">
              <p className="font-bold text-lg">
                Everything you need to know to stay on track
              </p>
              <p className="text-xs text-gray-500">
                Powerful features to help you and your team succeed everyday.
              </p>
            </div>
            {/* Card */}
            <div
              id="features"
              className="flex justify-around items-center mt-10 flex-nowrap gap-10 "
            >
              {/* Card 1 */}
              <FeatureCard
                title="Task Management"
                color="bg-blue-400"
                description="Create, organize, and prioritze tasks with ease."
                Icon={SquareCheckBig}
              />
              <FeatureCard
                title="Team Collaboration"
                color="bg-green-400"
                description="Work together seamlessly and get things done."
                Icon={Users}
              />
              <FeatureCard
                title="Progress Tracking"
                color="bg-orange-400"
                description="Visualize progress and meet deadlines."
                Icon={ChartNoAxesCombined}
              />
              <FeatureCard
                title="Reminders"
                color="bg-pink-400"
                description="Never miss a task with smart reminders."
                Icon={Bell}
              />
            </div>
          </div>
        </div>
      </section>
      {/* Boost  */}
      <section>
        <div className="w-full h-full p-10 bg-blue-50 rounded-lg shadow-sm shadow-blue-100">
          <div className="flex flex-col justify-center items-center">
            <h1 className="text-lg font-bold mb-2">
              Ready to boost your productivity?
            </h1>
            <p className="text-xs text-gray-500">
              Join thousands of teams already using Task Manager.
            </p>
            <a
              href="/signup"
              className="p-4 mt-5 bg-blue-400 rounded-lg text-gray-100 hover:bg-blue-300 cursor-pointer transition-colors ease-in-out delay-50 duration-200 "
            >
              Get Started — It's Free
            </a>
          </div>
        </div>
      </section>
      {/* Footer */}
      <footer>
        <div className="flex justify-between w-full h-full mt-10 flex-1 mb-2">
          {/* left */}
          <div className="flex flex-col justify-start items-start flex-1">
            <div className="flex mb-10">
              <SquareCheckBig color="#dbeafe" size={30} />
              <h1 className="ml-1 font-bold text-xl">TaskManager</h1>
            </div>
            <p className="text-gray-400 text-xs">
              &copy; 2026 Task Manager. All rights reserved.
            </p>
          </div>
          {/* middle */}
          <div className="flex justify-around items-start gap-20 flex-1">
            <div>
              <p className="font-bold">Product</p>
              <p>Features</p>
              <p>Pricing</p>
              <p>Changelog</p>
            </div>
            <div>
              <p className="font-bold">Resources</p>
              <p>Documentation</p>
              <a href="https://www.github.com/abdocodesc">
                <p>Github</p>
              </a>
              <p>Contact</p>
            </div>
          </div>
          {/* right */}
          <div className="flex flex-col gap-5 flex-1 justify-start items-end">
            <a href="https://www.github.com/abdocodesc">
              <svg
                fill="#000000"
                width="24px"
                height="24px"
                viewBox="0 0 25.00 25.00"
                xmlns="http://www.w3.org/2000/svg"
              >
                <g id="SVGRepo_bgCarrier" strokeWidth="0"></g>
                <g
                  id="SVGRepo_tracerCarrier"
                  strokeLinecap="round"
                  strokeLinejoin="round"
                ></g>
                <g id="SVGRepo_iconCarrier">
                  <path d="m12.301 0h.093c2.242 0 4.34.613 6.137 1.68l-.055-.031c1.871 1.094 3.386 2.609 4.449 4.422l.031.058c1.04 1.769 1.654 3.896 1.654 6.166 0 5.406-3.483 10-8.327 11.658l-.087.026c-.063.02-.135.031-.209.031-.162 0-.312-.054-.433-.144l.002.001c-.128-.115-.208-.281-.208-.466 0-.005 0-.01 0-.014v.001q0-.048.008-1.226t.008-2.154c.007-.075.011-.161.011-.249 0-.792-.323-1.508-.844-2.025.618-.061 1.176-.163 1.718-.305l-.076.017c.573-.16 1.073-.373 1.537-.642l-.031.017c.508-.28.938-.636 1.292-1.058l.006-.007c.372-.476.663-1.036.84-1.645l.009-.035c.209-.683.329-1.468.329-2.281 0-.045 0-.091-.001-.136v.007c0-.022.001-.047.001-.072 0-1.248-.482-2.383-1.269-3.23l.003.003c.168-.44.265-.948.265-1.479 0-.649-.145-1.263-.404-1.814l.011.026c-.115-.022-.246-.035-.381-.035-.334 0-.649.078-.929.216l.012-.005c-.568.21-1.054.448-1.512.726l.038-.022-.609.384c-.922-.264-1.981-.416-3.075-.416s-2.153.152-3.157.436l.081-.02q-.256-.176-.681-.433c-.373-.214-.814-.421-1.272-.595l-.066-.022c-.293-.154-.64-.244-1.009-.244-.124 0-.246.01-.364.03l.013-.002c-.248.524-.393 1.139-.393 1.788 0 .531.097 1.04.275 1.509l-.01-.029c-.785.844-1.266 1.979-1.266 3.227 0 .025 0 .051.001.076v-.004c-.001.039-.001.084-.001.13 0 .809.12 1.591.344 2.327l-.015-.057c.189.643.476 1.202.85 1.693l-.009-.013c.354.435.782.793 1.267 1.062l.022.011c.432.252.933.465 1.46.614l.046.011c.466.125 1.024.227 1.595.284l.046.004c-.431.428-.718 1-.784 1.638l-.001.012c-.207.101-.448.183-.699.236l-.021.004c-.256.051-.549.08-.85.08-.022 0-.044 0-.066 0h.003c-.394-.008-.756-.136-1.055-.348l.006.004c-.371-.259-.671-.595-.881-.986l-.007-.015c-.198-.336-.459-.614-.768-.827l-.009-.006c-.225-.169-.49-.301-.776-.38l-.016-.004-.32-.048c-.023-.002-.05-.003-.077-.003-.14 0-.273.028-.394.077l.007-.003q-.128.072-.08.184c.039.086.087.16.145.225l-.001-.001c.061.072.13.135.205.19l.003.002.112.08c.283.148.516.354.693.603l.004.006c.191.237.359.505.494.792l.01.024.16.368c.135.402.38.738.7.981l.005.004c.3.234.662.402 1.057.478l.016.002c.33.064.714.104 1.106.112h.007c.045.002.097.002.15.002.261 0 .517-.021.767-.062l-.027.004.368-.064q0 .609.008 1.418t.008.873v.014c0 .185-.08.351-.208.466h-.001c-.119.089-.268.143-.431.143-.075 0-.147-.011-.214-.032l.005.001c-4.929-1.689-8.409-6.283-8.409-11.69 0-2.268.612-4.393 1.681-6.219l-.032.058c1.094-1.871 2.609-3.386 4.422-4.449l.058-.031c1.739-1.034 3.835-1.645 6.073-1.645h.098-.005zm-7.64 17.666q.048-.112-.112-.192-.16-.048-.208.032-.048.112.112.192.144.096.208-.032zm.497.545q.112-.08-.032-.256-.16-.144-.256-.048-.112.08.032.256.159.157.256.047zm.48.72q.144-.112 0-.304-.128-.208-.272-.096-.144.08 0 .288t.272.112zm.672.673q.128-.128-.064-.304-.192-.192-.32-.048-.144.128.064.304.192.192.32.044zm.913.4q.048-.176-.208-.256-.24-.064-.304.112t.208.24q.24.097.304-.096zm1.009.08q0-.208-.272-.176-.256 0-.256.176 0 .208.272.176.256.001.256-.175zm.929-.16q-.032-.176-.288-.144-.256.048-.224.24t.288.128.225-.224z"></path>
                </g>
              </svg>
            </a>
            <a href="https://www.linkedin.com/in/abderrahmane-chaibe">
              <svg
                fill="#000000"
                width="24px"
                height="24px"
                viewBox="0 -0.5 25 25"
                xmlns="http://www.w3.org/2000/svg"
              >
                <g id="SVGRepo_bgCarrier" strokeWidth="0"></g>
                <g
                  id="SVGRepo_tracerCarrier"
                  strokeLinecap="round"
                  strokeLinejoin="round"
                ></g>
                <g id="SVGRepo_iconCarrier">
                  <path d="m5.706 7.798v16.202h-5.395v-16.202zm.343-5.002c.001.029.002.063.002.098 0 .749-.318 1.423-.826 1.895l-.002.001c-.545.498-1.274.803-2.075.803-.049 0-.099-.001-.148-.003h.007-.033c-.041.002-.089.003-.137.003-.784 0-1.496-.306-2.025-.804l.001.001c-.504-.488-.816-1.17-.816-1.925 0-.024 0-.048.001-.073v.004c-.001-.021-.001-.045-.001-.069 0-.762.324-1.448.841-1.929l.002-.001c.544-.495 1.271-.799 2.068-.799.046 0 .091.001.137.003h-.006c.043-.002.092-.003.143-.003.785 0 1.5.303 2.034.798l-.002-.002c.515.497.835 1.193.835 1.964v.042-.002zm19.062 11.92v9.284h-5.378v-8.665c.005-.079.007-.171.007-.263 0-.896-.249-1.733-.682-2.447l.012.021c-.427-.596-1.117-.979-1.896-.979-.06 0-.12.002-.18.007h.008c-.027-.001-.058-.002-.089-.002-.62 0-1.19.213-1.641.57l.006-.004c-.453.367-.808.836-1.032 1.375l-.008.023c-.116.355-.182.763-.182 1.187 0 .048.001.096.003.144v-.007 9.042h-5.378q.033-6.523.033-10.578t-.016-4.839l-.016-.785h5.378v2.354h-.033c.214-.345.435-.644.678-.924l-.008.009c.281-.309.583-.588.908-.838l.016-.012c.404-.311.878-.555 1.392-.704l.03-.007c.538-.161 1.157-.254 1.797-.254h.079-.004c.071-.003.154-.005.237-.005 1.681 0 3.195.714 4.256 1.856l.003.004q1.702 1.856 1.702 5.436z"></path>
                </g>
              </svg>
            </a>
            <a href="mailto:abderrahmanechaibe@gmail.com">
              <Mail />
            </a>
          </div>
        </div>
      </footer>
    </div>
  );
}

export default Home;
