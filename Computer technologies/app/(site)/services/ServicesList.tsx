"use client";

import Link from "next/link";
import { useLeadModal } from "@/components/providers/LeadModalProvider";
import type { Service } from "@/payload-types";

export default function ServicesList({ services }: { services: Service[] }) {
  const { openModal } = useLeadModal();
  
  
  const halls = Array.from(new Set(services.map((s) => s.hall)));

  return (
    <div className="max-w-6xl mx-auto py-16 px-4">
      <div className="text-center mb-12">
        <h1 className="text-4xl font-bold text-vilet-green mb-4">Наши услуги</h1>
        <p className="text-gray-600 max-w-2xl mx-auto">
          Мы разделили наш салон на уютные залы, чтобы вы чувствовали себя максимально комфортно. Выберите подходящую услугу.
        </p>
      </div>

      {halls.map((hall) => (
        <div key={hall} className="mb-16">
          <h2 className="text-2xl font-bold text-vilet-green border-b border-gray-300 pb-2 mb-6">
            {hall}
          </h2>
          
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {services
              .filter((service) => service.hall === hall)
              .map((service) => (
                <div key={service.id} className="bg-white rounded-xl shadow-sm border border-gray-100 overflow-hidden hover:shadow-md transition-shadow flex flex-col">
                  <div className="p-6 flex-grow">
                    <h3 className="text-xl font-bold text-gray-800 mb-2">{service.title}</h3>
                    <p className="text-gray-500 text-sm mb-4 line-clamp-2">{service.description}</p>
                    
                    <div className="flex justify-between items-center mt-auto pt-4 border-t border-gray-100">
                      <span className="font-bold text-vilet-green text-lg">{service.price} ₽</span>
                      <span className="text-gray-400 text-sm">{service.duration}</span>
                    </div>
                  </div>
                  
                  <div className="p-4 bg-gray-50 flex gap-2">
                    <Link 
                      href={`/services/${service.slug}`}
                      className="flex-1 text-center bg-white border border-gray-300 text-gray-700 py-2 rounded-lg text-sm hover:bg-gray-100 transition-colors"
                    >
                      Подробнее
                    </Link>
                    <button 
                      onClick={openModal}
                      className="flex-1 text-center bg-vilet-green text-white py-2 rounded-lg text-sm hover:bg-opacity-90 transition-colors cursor-pointer"
                    >
                      Записаться
                    </button>
                  </div>
                </div>
              ))}
          </div>
        </div>
      ))}
    </div>
  );
}