"use client";

import { useState } from "react";
import { useLeadModal } from "@/components/providers/LeadModalProvider";
import type { Service } from "@/payload-types";

export default function PricesTable({ services }: { services: Service[] }) {
  const { openModal } = useLeadModal();
  const [searchTerm, setSearchTerm] = useState("");

  const filteredServices = services.filter((service) =>
    service.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
    service.hall.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <div className="max-w-4xl mx-auto py-16 px-4">
      <h1 className="text-4xl font-bold text-vilet-green mb-8 text-center">Цены на услуги</h1>
      
      <div className="mb-8 relative">
        <input
          type="text"
          placeholder="Поиск по названию или залу (например, 'стрижка')..."
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          className="w-full px-4 py-3 rounded-xl border border-gray-300 focus:outline-none focus:ring-2 focus:ring-vilet-gold shadow-sm"
        />
        <svg className="w-5 h-5 text-gray-400 absolute right-4 top-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path>
        </svg>
      </div>

      <div className="bg-white rounded-xl shadow-sm border border-gray-100 overflow-hidden">
        <table className="w-full text-left border-collapse">
          <thead>
            <tr className="bg-vilet-green text-white">
              <th className="p-4 font-medium">Услуга</th>
              <th className="p-4 font-medium hidden md:table-cell">Зал</th>
              <th className="p-4 font-medium">Время</th>
              <th className="p-4 font-medium">Цена</th>
              <th className="p-4 font-medium text-center">Запись</th>
            </tr>
          </thead>
          <tbody>
            {filteredServices.length > 0 ? (
              filteredServices.map((service) => (
                <tr key={service.id} className="border-b border-gray-100 hover:bg-gray-50 transition-colors">
                  <td className="p-4">
                    <div className="font-bold text-gray-800">{service.title}</div>
                    <div className="text-sm text-gray-500 md:hidden">{service.hall}</div>
                  </td>
                  <td className="p-4 hidden md:table-cell text-gray-600">{service.hall}</td>
                  <td className="p-4 text-gray-600">{service.duration}</td>
                  <td className="p-4 font-bold text-vilet-green">{service.price} ₽</td>
                  <td className="p-4 text-center">
                    <button 
                      onClick={openModal}
                      className="bg-vilet-beige text-vilet-green px-4 py-1.5 rounded-full text-sm font-medium hover:bg-vilet-gold hover:text-white transition-colors cursor-pointer"
                    >
                      Записаться
                    </button>
                  </td>
                </tr>
              ))
            ) : (
              <tr>
                <td colSpan={5} className="p-8 text-center text-gray-500">
                  По вашему запросу ничего не найдено.
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}