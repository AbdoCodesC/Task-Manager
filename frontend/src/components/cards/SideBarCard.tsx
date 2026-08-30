import React from "react";
import { type LucideProps } from "../../types";

function SideBarCard({
  Icon,
  title,
  handleView
}: {
  Icon: React.FC<LucideProps>;
  title: string;
  handleView: (component: string) => void
}) {
  return (
    <button className="hover:bg-blue-100 w-full flex gap-2  items-center cursor-pointer p-3 rounded-md" onClick={() => handleView(title.toLowerCase())}>
      <Icon size={20} color="darkgray" />
      <p className="text-md text-gray-500">{title}</p>
    </button>
  );
}

export default SideBarCard;
