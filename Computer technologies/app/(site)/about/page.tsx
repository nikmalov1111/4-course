import Image from "next/image";
import { getPayloadClient } from "@/lib/payload";
import type { Metadata } from "next";

export const dynamic = 'force-dynamic';

export const metadata: Metadata = {
  title: "О нас | Парикмахерская Vilet",
  description: "Узнайте больше о парикмахерской Vilet: наши ценности, атмосфера, опытные мастера и преимущества перед конкурентами.",
};

export default async function AboutPage() {
  const payload = await getPayloadClient();
  const about = await payload.findGlobal({ slug: 'about-page' });

  return (
    <div className="max-w-6xl mx-auto py-16 px-4">
      <div className="text-center max-w-3xl mx-auto mb-16">
        <h1 className="text-4xl md:text-5xl font-bold text-vilet-green mb-6">
          {about.title}
        </h1>
        <p className="text-lg text-gray-600 leading-relaxed whitespace-pre-line">
          {about.intro}
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-12 items-center mb-20">
        <div className="relative h-[400px] rounded-2xl overflow-hidden shadow-lg bg-gray-200">
          {about.image && typeof about.image === 'object' && about.image.url ? (
            <Image
              src={about.image.url}
              alt={about.image.alt || "Интерьер салона Vilet"}
              fill
              className="object-cover"
              unoptimized 
            />
          ) : (
            <div className="w-full h-full flex items-center justify-center text-gray-400">Нет фото</div>
          )}
        </div>
        <div>
          <h2 className="text-2xl font-bold text-vilet-green mb-4">Атмосфера и качество</h2>
          <p className="text-gray-600 mb-4 leading-relaxed">
            Мы верим, что поход к парикмахеру — это не просто рутина, а маленький праздник.
            В нашем салоне вы можете расслабиться за чашкой ароматного кофе или чая, пока наши мастера создают вашу новую прическу.
          </p>
          <p className="text-gray-600 leading-relaxed">
            Мы используем только премиальную профессиональную косметику, которая бережно ухаживает за волосами и дает длительный результат.
          </p>
        </div>
      </div>

      <div className="bg-white rounded-2xl p-8 md:p-12 shadow-sm border border-gray-100">
        <h2 className="text-2xl font-bold text-vilet-green mb-8 text-center">Почему выбирают нас</h2>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-8 text-center">
          {about.advantages?.map((adv, idx) => (
            <div key={idx}>
              <div className="w-16 h-16 bg-vilet-beige rounded-full flex items-center justify-center mx-auto mb-4">
                <svg className="w-8 h-8 text-vilet-green" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 13l4 4L19 7" />
                </svg>
              </div>
              <h3 className="font-bold text-lg mb-2">{adv.title}</h3>
              <p className="text-gray-500 text-sm">{adv.description}</p>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}