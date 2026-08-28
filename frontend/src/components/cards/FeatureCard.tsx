import React from "react";
import { type LucideProps } from "../../types";

function FeatureCard({
  Icon,
  title,
  description,
  color
}: {
  Icon: React.FC<LucideProps>;
  title: string;
  description: string;
  color: string;
}) {
  return (
    <div className="flex items-center justify-center flex-col  p-10 rounded-md shadow-md shadow-black flex-1">
      <div className={`flex justify-center items-center mb-5 ${color} p-2 rounded-md`}>{<Icon strokeWidth={2} size={30} color="white"/>}</div>
      <h1 className="mb-5 font-bold text-md">{title}</h1>
      <p className="text-sm text-gray-500">{description}</p>
    </div>
  );
}

export default FeatureCard;
