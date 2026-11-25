import { getPayloadClient } from "@/lib/payload";
import ServiceBookingButton from "@/components/ServiceBookingButton";
import type { Metadata } from "next";

export const dynamic = 'force-dynamic';

export const metadata: Metadata = {
  title: "Контакты | Парикмахерская Vilet",
  description: "Адрес, телефон, режим работы и карта проезда до парикмахерской Vilet в Вологде. Свяжитесь с нами или оставьте заявку.",
};

export default async function ContactsPage() {
  const payload = await getPayloadClient();
  const contacts = await payload.findGlobal({ slug: 'contacts' });

  const mapSrc = contacts.mapCoordinates
    ? `https://yandex.ru/map-widget/v1/?ll=${contacts.mapCoordinates.split(',').join('%2C')}&z=15&pt=${contacts.mapCoordinates}`
    : "https://yandex.ru/map-widget/v1/?ll=39.911661%2C59.187097&z=15&pt=39.911661,59.187097,pm2rdm";

  return (
    <div className="max-w-6xl mx-auto py-16 px-4">
      <h1 className="text-4xl font-bold text-vilet-green mb-8 text-center">Контакты</h1>

      <div className="bg-white rounded-2xl shadow-sm border border-gray-100 overflow-hidden flex flex-col lg:flex-row">
        <div className="lg:w-1/3 p-8 md:p-12 flex flex-col justify-between bg-white border-b lg:border-b-0 lg:border-r border-gray-100">
          <div>
            <h2 className="text-2xl font-bold text-gray-800 mb-6">Парикмахерская Vilet</h2>

            <div className="space-y-6 text-gray-600">
              <div>
                <p className="text-sm font-bold text-vilet-gold uppercase tracking-wider mb-1">Адрес</p>
                <p className="text-lg">{contacts.address}</p>
              </div>

              <div>
                <p className="text-sm font-bold text-vilet-gold uppercase tracking-wider mb-1">Телефон</p>
                <a href={`tel:${contacts.phone?.replace(/[^+\d]/g, '')}`} className="text-xl font-medium hover:text-vilet-green transition-colors">
                  {contacts.phone}
                </a>
              </div>

              <div>
                <p className="text-sm font-bold text-vilet-gold uppercase tracking-wider mb-1">Режим работы</p>
                <p className="text-lg whitespace-pre-line">{contacts.schedule}</p>
              </div>
            </div>
          </div>

          <div className="mt-8">
            <p className="text-sm text-gray-500 mb-3">Остались вопросы? Мы перезвоним!</p>
            <ServiceBookingButton />
          </div>
        </div>

        <div className="lg:w-2/3 min-h-[400px] relative bg-gray-100">
          <iframe
            src={mapSrc}
            width="100%"
            height="100%"
            frameBorder="0"
            allowFullScreen={true}
            className="absolute inset-0 w-full h-full"
            title="Карта расположения салона"
          ></iframe>
        </div>
      </div>
    </div>
  );
}