import type { Metadata } from "next";
import "./globals.css";
import Sidebar from "@/components/Sidebar";
import PulseFeed from "@/components/PulseFeed";
import CommandCenter from "@/components/CommandCenter";

export const metadata: Metadata = {
  title: "Aether | Autonomous Startup Engine",
  description: "A production-grade autonomous startup engine inspired by Emergent and Polsia.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className="void-gradient">
        <Sidebar />
        <main style={{ 
          marginLeft: 'var(--sidebar-width)', 
          marginRight: 'var(--pulse-width)',
          height: '100vh',
          overflowY: 'auto',
          position: 'relative'
        }}>
          {children}
          <CommandCenter />
        </main>
        <PulseFeed />
      </body>
    </html>
  );
}
