import { locales } from 'langs/locales.json';

export const getStaticPaths = () => {
  const list: { params: { lang: string | undefined } }[] = [];
  for (let x in locales) list.push({ params: { lang: x } });
  list.push({ params: { lang: undefined } });
  return list;
};
