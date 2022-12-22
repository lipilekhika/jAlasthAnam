import links from './links.json';
import { val_from_adress } from 'tools/json';

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
export const replace_link_text = (vl: string) => {
  const template = (link: string) => `](${link})`;
  const regex = /\]\(links:.+?\)/g;
  const match = reg_index(vl, regex);
  try {
    links.mukhya.web_app = import.meta.env.PUBLIC_SITE_URL1! || '';
    links.mukhya.web_site = import.meta.env.PUBLIC_SITE_URL! || '';
    // CAUTION :- This needs to be updated as per the project
  } catch {}
  let ind_change = 0;
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
