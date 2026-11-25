"use client";

import { useLeadModal } from "@/components/providers/LeadModalProvider";
import type { Promotion } from "@/payload-types";

export default function PromotionsList({ promotions }: { promotions: Promotion[] }) {
  const { openModal } = useLeadModal();

  return (
    <div className="max-w-6xl mx-auto py-16 px-4">
      <div className="text-center mb-12">
        <h1 className="text-4xl font-bold text-vilet-green mb-4">Акции и спецпредложения</h1>
        <p className="text-gray-600 max-w-2xl mx-auto">
          Мы регулярно радуем наших гостей приятными бонусами. Следите за обновлениями!
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
        {promotions.map((promo) => {
          const imageUrl = typeof promo.image === 'object' && promo.image?.url 
            ? promo.image.url 
            : null;

          return (
            <div key={promo.id} className="bg-white rounded-2xl shadow-sm border border-gray-100 overflow-hidden flex flex-col relative group hover:shadow-md transition-shadow">
              
              {promo.badge && (
                <div className="absolute top-4 right-4 bg-vilet-gold text-white text-xs font-bold px-3 py-1 rounded-full z-10 shadow-sm">
                  {promo.badge}
                </div>
              )}

              <div className="h-48 bg-vilet-beige relative flex items-center justify-center overflow-hidden">
                {imageUrl ? (
                  <img 
                    src={imageUrl} 
                    alt={promo.title} 
                    className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500" 
                  />
                ) : (
                  <svg className="w-16 h-16 text-vilet-green opacity-20" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 8v13m0-13V6a2 2 0 112 2h-2zm0 0V5.5A2.5 2.5 0 109.5 8H12zm-7 4h14M5 12a2 2 0 110-4h14a2 2 0 110 4M5 12v7a2 2 0 002 2h10a2 2 0 002-2v-7" />
                  </svg>
                )}
              </div>

              <div className="p-6 flex-grow flex flex-col">
                <h3 className="text-xl font-bold text-gray-800 mb-2">{promo.title}</h3>
                <p className="text-gray-500 text-sm mb-6 flex-grow whitespace-pre-line">{promo.description}</p>
                
                <button 
                  onClick={openModal}
                  className="w-full bg-vilet-green text-white py-2.5 rounded-xl font-medium hover:bg-opacity-90 transition-colors cursor-pointer"
                >
                  Уточнить условия
                </button>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}