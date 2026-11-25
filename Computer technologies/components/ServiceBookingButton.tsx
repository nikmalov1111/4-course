"use client";

import { useLeadModal } from "@/components/providers/LeadModalProvider";

export default function ServiceBookingButton() {
  const { openModal } = useLeadModal();

  return (
    <button 
      onClick={openModal}
      className="px-8 py-3 bg-vilet-green text-white rounded-full font-medium hover:bg-opacity-90 transition-colors shadow-lg cursor-pointer"
    >
      Записаться на услугу
    </button>
  );
}