import { locales, default_locale } from 'langs/locales.json';

export const getStaticPaths = () => {
  const list: { params: { lang: string | undefined } }[] = [];
  for (let x in locales) {
    if (x === default_locale) continue;
    list.push({ params: { lang: x } });
  }
  list.push({ params: { lang: undefined } });
  return list;
};
