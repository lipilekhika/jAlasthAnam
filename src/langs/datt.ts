import { locales } from './locales.json';
import { load } from 'js-yaml';
import { set_val_from_adress, val_from_adress, process_json } from 'tools/json';
import * as fs from 'fs';
import Markdown from 'markdown-it';
import links from './links.json';
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
const reg_index = (str: string, pattern: RegExp) => {
  let ind: [number, string][] = [],
    mtch: RegExpExecArray = null!;
  while ((mtch = pattern.exec(str)!) != null) ind.push([mtch.index, mtch[0]]);
  return ind;
};
const substring = (val: string, from = 0, to: number = null!) => {
  if (to == null) to = val.length;
  if (to > 0) return val.substring(from, to);
  else if (to < 0) return val.substring(from, val.length + to);
};
const replace_link_text = (vl: string) => {
  const template = (link: string) => `](${link})`;
  const regex = /\]\(links:.+?\)/g;
  const match = reg_index(vl, regex);
  let ind_change = 0;
  try {
    links.mukhya.web_app = import.meta.env.PUBLIC_SITE_URL1! || '';
    links.mukhya.web_site = import.meta.env.PUBLIC_SITE_URL! || '';
    // CAUTION :- This needs to be updated as per the project
  } catch {}
  for (let x of match) {
    let address = (() => {
      let v = substring(x[1], 8, -1);
      if (!v?.startsWith('/')) v = '/' + v;
      return v;
    })();
    let link = val_from_adress(address, links);
    let _new = template(link);
    let ind = [x[0] + ind_change, x[0] + x[1].length + ind_change];
    let st = vl.substring(0, ind[0]);
    let end = vl.substring(ind[0] + x[1].length);
    vl = st + _new + end;
    ind_change += _new.length - (ind[1] - ind[0]);
  }
  return vl;
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
