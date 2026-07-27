import type { Metadata } from "next";
import { FactorySite } from "./site";

type SearchParams = Promise<{ lang?: string }>;

export async function generateMetadata({
  searchParams,
}: {
  searchParams: SearchParams;
}): Promise<Metadata> {
  const { lang } = await searchParams;
  const spanish = lang === "es";
  const title = spanish
    ? "Factory — Entrega de software dirigida por humanos y ejecutada por IA"
    : "Factory — Human-directed, AI-executed software delivery";
  const description = spanish
    ? "Un sistema operativo de código abierto para equipos donde la IA realiza el trabajo técnico principal y las personas mantienen el control."
    : "An open-source operating system for teams where AI performs the principal technical work and humans remain in control.";

  return {
    title,
    description,
    alternates: {
      canonical: "/",
      languages: { en: "/?lang=en", es: "/?lang=es" },
    },
    openGraph: {
      title,
      description,
      type: "website",
      images: [{ url: "/og.png", width: 1200, height: 630 }],
    },
    twitter: {
      card: "summary_large_image",
      title,
      description,
      images: ["/og.png"],
    },
  };
}

export default async function Home({
  searchParams,
}: {
  searchParams: SearchParams;
}) {
  const { lang } = await searchParams;
  return <FactorySite initialLanguage={lang === "es" ? "es" : "en"} />;
}
