// Languages with a regional variant, named like the folders in public/i18n.
const REGIONAL = ["pt_BR"];

// The browser's language as a folder name: "pt-BR" gives "pt_BR" when that
// translation exists, and the two-letter code otherwise.
export function browserLanguage(tag = navigator.language) {
  const [language, region] = (tag || "en").split("-");
  const regional = region
    ? `${language.toLowerCase()}_${region.toUpperCase()}`
    : "";
  return REGIONAL.includes(regional) ? regional : language.toLowerCase();
}

export async function loadLanguage(lang) {
  try {
    const messages = await import(
      /* webpackChunkName: "lang-[request]" */ `../../public/i18n/${lang}/translation.json`
    );
    return messages;
  } catch (error) {
    console.warn(
      `Cannot import ${lang} language messages, falling back to English.`,
      error
    );

    // fallback to english
    if (lang !== "en") {
      return loadLanguage("en");
    }
  }
}
