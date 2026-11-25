import Link from "next/link";
import type { Master } from "@/payload-types";

export default function MastersList({ masters }: { masters: Master[] }) {
  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
      {masters.map((master) => {

        const imageUrl = typeof master.image === 'object' && master.image?.url 
          ? master.image.url 
          : '/placeholder.jpg';

        return (
          <Link
            href={`/masters/${master.slug}`}
            key={master.id}
            className="group bg-white rounded-2xl overflow-hidden shadow-sm hover:shadow-xl transition-all duration-300 border border-gray-100"
          >
            <div className="relative h-80 w-full overflow-hidden bg-gray-200">
              <img
                src={imageUrl}
                alt={master.name}
                className="absolute inset-0 w-full h-full object-cover group-hover:scale-105 transition-transform duration-500"
              />
            </div>
            <div className="p-6 text-center">
              <h3 className="text-xl font-bold text-gray-800 mb-1">{master.name}</h3>
              <p className="text-vilet-gold font-medium mb-3">{master.role}</p>
              <p className="text-sm text-gray-500">Опыт работы: {master.experience}</p>
            </div>
          </Link>
        );
      })}
    </div>
  );
}