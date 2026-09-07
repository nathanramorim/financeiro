import type { Metadata, Viewport } from "next";
import { Montserrat } from "next/font/google";
import { AppChrome } from "@/components/layout/AppChrome";
import "./globals.css";

const montserrat = Montserrat({
  subsets: ["latin"],
  weight: ["300", "400", "500", "600", "700"],
  variable: "--font-montserrat",
  display: "swap",
});

export const metadata: Metadata = {
  title: "Assistente Financeiro Inteligente",
  description: "Gestão financeira pessoal com inteligência artificial, regras guardrail e integração Google Sheets",
};

export const viewport: Viewport = {
  width: "device-width",
  initialScale: 1,
  maximumScale: 1,
  viewportFit: "cover",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="pt-BR" className={montserrat.variable}>
      <body className="min-h-screen bg-panel text-text font-sans antialiased">
        <AppChrome>{children}</AppChrome>
      </body>
    </html>
  );
}
