function StatusCard({
  title,
  handleFilter,
  filter,
}: {
  title: string;
  handleFilter: (filter: string) => void;
  filter: string;
}) {
  return (
    <button
      className={`cursor-pointer p-1 border-b-2 ${filter === title.toLowerCase() ? " border-blue-200" : "border-transparent"}`}
      onClick={() => handleFilter(title.toLowerCase())}
    >
      {title}
    </button>
  );
}

export default StatusCard;
