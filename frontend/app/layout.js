import { Inter } from "next/font/google";
import "./globals.css";
import SessionWrapper from "./components/SessionWrapper";
import NavBar from "./components/NavBar";
const inter = Inter({ subsets: ["latin"] });

export default function RootLayout({ children }) {
  return (
    <SessionWrapper>
      <html lang="en">
        <body className={inter.className}>
          <NavBar />
          <div>{children}</div>
        </body>
      </html>
    </SessionWrapper>
  );
}
