import type { Metadata } from "next";
import { Geist } from "next/font/google";
import "../globals.css";
import Header from "@/components/layout/Header";
import Footer from "@/components/layout/Footer";
import { LeadModalProvider } from "@/components/providers/LeadModalProvider";
import { getPayloadClient } from "@/lib/payload";

export const dynamic = 'force-dynamic';

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "Парикмахерская Vilet | Стрижки, окрашивание, уход",
  description: "Современная парикмахерская Vilet. Профессиональные мастера, премиальный уход и онлайн-запись.",
};

export default async function SiteLayout({ children }: { children: React.ReactNode }) {
  const payload = await getPayloadClient();
  const contacts = await payload.findGlobal({ slug: 'contacts' });

  const safeContacts = contacts || {
    phone: "+7 (921) 541-87-67",
    schedule: "Пн-Сб с 09:00 до 19:00\nВоскресенье с 09:00 до 18:00",
  };

  return (
    <html lang="ru" className={`${geistSans.variable} h-full antialiased`}>
      <body className="min-h-full flex flex-col">
        <LeadModalProvider>
          <Header />
          <main className="flex-grow">
            {children}
          </main>
          <Footer contacts={safeContacts} />
        </LeadModalProvider>
      </body>
    </html>
  );
}