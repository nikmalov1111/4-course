"use client";

import { useLeadModal } from "@/components/providers/LeadModalProvider";

export default function HomeCta({ label }: { label: string }) {
  const { openModal } = useLeadModal();
  
  return (
    <button 
      onClick={openModal}
      className="inline-block bg-vilet-gold text-white px-8 py-3 rounded-full text-lg font-medium hover:bg-yellow-600 transition-colors shadow-lg hover:shadow-xl cursor-pointer"
    >
      {label}
    </button>
  );
}