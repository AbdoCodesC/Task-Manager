function ProjectCard({ bgColor, title }: { bgColor: string; title: string }) {
  return (
    <div className="flex gap-5 items-center">
      <div className={`w-3 h-3 rounded-full ${bgColor}`}></div>
      <a href="/link">
        <p className="text-gray-600 hover:underline">{title}</p>
      </a>
    </div>
  );
}

export default ProjectCard;
