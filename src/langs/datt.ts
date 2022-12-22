import { locales } from './locales.json';
import { load } from 'js-yaml';
import { set_val_from_adress, process_json } from 'tools/json';
import * as fs from 'fs';
import Markdown from 'markdown-it';
import { replace_link_text } from './process';
import type { dattType } from './model';
export type { dattType } from './model';

const md = new Markdown();

export type langKey = keyof typeof locales; // Language list
export const langNames = Object.values(locales);

const reuseValues = (datt: dattType) => {
  const reuseMap: [string, string[]][] = [];
  for (let x of reuseMap)
    for (let y of x[1]) set_val_from_adress(y.substring(4).split('.').join('/'), datt, x[0]);
  return datt;
};
const db: { [x in langKey]?: dattType } = {};
const markdownify_keys = (val: string) => {
  let res = md.render(val);
  if (res.startsWith('<p>') && res.endsWith('</p>\n')) res = res.substring(3, res.length - 5);
  return res;
};
const main = (locale: langKey, type = '') => {
  if (import.meta.env.PROD && locale in db) return db[locale];
  const STR_LOADED = replace_link_text(
    fs.readFileSync(`./src/langs/data/${locales[locale]}.yaml`).toString()
  );
  let dt = process_json(reuseValues(load(STR_LOADED) as dattType), markdownify_keys) as dattType;
  db[locale] = dt;
  return dt;
};
export default main;
