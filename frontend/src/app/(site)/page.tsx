import Home from "@/components/Home";
import { Metadata } from "next";

export const metadata: Metadata = {
  title: "Al Makkah Electronics - Home",
  description: "Shop the latest electronics at Al Makkah Electronics.",

};

export default function HomePage() {
  return (
    <>
      <Home />
    </>
  );
}
