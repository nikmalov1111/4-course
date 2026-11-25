import { Suspense } from 'react';
import { getPayloadClient } from '@/lib/payload';
import MastersList from './MastersList';
import type { Metadata } from "next";

export const dynamic = 'force-dynamic';


export const metadata: Metadata = {
  title: "Наши мастера | Парикмахерская Vilet",
  description: "Команда опытных стилистов, колористов и барберов парикмахерской Vilet. Выберите своего мастера и запишитесь онлайн.",
};


export default function MastersPage() {
  return (
    <div className="max-w-6xl mx-auto py-16 px-4">
      <div className="text-center mb-12">
        <h1 className="text-4xl font-bold text-vilet-green mb-4">Наши мастера</h1>
        <p className="text-gray-600 max-w-2xl mx-auto">
          Команда профессионалов, влюбленных в свое дело. Выберите своего мастера, чтобы узнать о нем больше.
        </p>
      </div>

      <Suspense fallback={<div className="text-center py-20 text-gray-500">Загрузка мастеров...</div>}>
        <MastersContent />
      </Suspense>
    </div>
  );
}

async function MastersContent() {
  const payload = await getPayloadClient();
  
  const { docs: masters } = await payload.find({ 
    collection: 'masters',
    limit: 200, 
  });

  return <MastersList masters={masters} />;
}