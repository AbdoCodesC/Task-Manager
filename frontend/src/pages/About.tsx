import { User } from "lucide-react";

function About() {
  return (
    <div className="flex justify-between w-full h-screen overflow-hidden">
      {/* Left */}
      <div className="flex flex-col gap-20 flex-1 p-5">
        <p className="font-bold text-4xl">
          About <a href="/">TaskManager</a>
        </p>
        <p className="mt-5 text-lg">
          <span className="font-bold text-xl underline">TaskManager</span> is a
          modern task management application designed to help individuals and
          teams stay organized and productive.
        </p>
        <div className="flex flex-col gap-8 w-full ">
          <AboutCard title="Organize tasks and projects" />
          <AboutCard title="Collaborate with team members" />
          <AboutCard title="Track progress and productivity" />
          <AboutCard title="Meet deadlines and goals" />
        </div>
      </div>
      {/* Right */}
      <div className="flex w-full justify-center items-center flex-1 p-5">
        <img src="/about.svg" alt="" />
      </div>
    </div>
  );
}

function AboutCard({ title }: { title: string }) {
  return (
    <div className="flex justify-start items-center gap-5 w-full py-1">
      <div className="p-1 items-center justify-center bg-gray-200 rounded-full">
        <User size={40} />
      </div>
      <p className="text-lg">{title}</p>
    </div>
  );
}

export default About;
