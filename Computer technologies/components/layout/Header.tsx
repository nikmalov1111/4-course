"use client";

import Link from "next/link";
import { useState } from "react";
import { useLeadModal } from "@/components/providers/LeadModalProvider";

const navLinks = [
  { name: "Услуги", href: "/services" },
  { name: "Цены", href: "/prices" },
  { name: "Акции", href: "/promotions" },
  { name: "Мастера", href: "/masters" },
  { name: "О нас", href: "/about" },
  { name: "Контакты", href: "/contacts" },
];

export default function Header() {
  const { openModal } = useLeadModal();
  const [isMenuOpen, setIsMenuOpen] = useState(false);

  const closeMenu = () => setIsMenuOpen(false);

  const handleBookClick = () => {
    closeMenu();
    openModal();
  };

  return (
    <header className="bg-white shadow-sm sticky top-0 z-50">
      <div className="max-w-6xl mx-auto px-4 py-4 flex justify-between items-center">
        
        <Link href="/" className="text-2xl font-bold tracking-widest text-vilet-green" onClick={closeMenu}>
          VILET
        </Link>

        <nav className="hidden md:flex gap-6 font-medium">
          {navLinks.map((link) => (
            <Link key={link.href} href={link.href} className="hover:text-vilet-gold transition-colors">
              {link.name}
            </Link>
          ))}
        </nav>

        <button
          onClick={openModal}
          className="hidden md:block bg-vilet-green text-white px-6 py-2 rounded-full hover:bg-opacity-90 transition-all cursor-pointer"
        >
          Записаться
        </button>

        <button
          className="md:hidden text-vilet-green p-2 focus:outline-none"
          onClick={() => setIsMenuOpen(!isMenuOpen)}
          aria-label="Открыть меню"
        >
          {isMenuOpen ? (
            <svg className="w-7 h-7" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          ) : (
            <svg className="w-7 h-7" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M4 6h16M4 12h16M4 18h16" />
            </svg>
          )}
        </button>
      </div>

      {isMenuOpen && (
        <div className="md:hidden bg-white border-t border-gray-100 absolute w-full left-0 shadow-lg">
          <nav className="flex flex-col px-4 py-4 space-y-4">
            {navLinks.map((link) => (
              <Link
                key={link.href}
                href={link.href}
                className="text-lg font-medium text-gray-800 hover:text-vilet-gold transition-colors"
                onClick={closeMenu}
              >
                {link.name}
              </Link>
            ))}
            
            <div className="pt-4 border-t border-gray-100">
              <button
                onClick={handleBookClick}
                className="w-full bg-vilet-green text-white px-6 py-3 rounded-full font-medium hover:bg-opacity-90 transition-all"
              >
                Записаться
              </button>
            </div>
          </nav>
        </div>
      )}
    </header>
  );
}