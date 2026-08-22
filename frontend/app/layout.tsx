import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Triangle Tic-Tac-Toe",
  description: "A new angle on the classic three-in-a-row game.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
