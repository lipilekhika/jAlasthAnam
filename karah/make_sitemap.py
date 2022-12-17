import json
import jinja2
import os
import shutil


def write(loc, val):
    f = open(loc, encoding="utf-8", mode="w")
    f.write(val)
    f.close()


def read(loc):
    f = open(loc, encoding="utf-8", mode="r")
    vl = f.read()
    f.close()
    return vl


def delete_folder(loc):
    try:
        shutil.rmtree(loc)
    except:
        pass


def render(fl, **o):
    return (
        jinja2.Environment(loader=jinja2.FileSystemLoader("./karah/template"))
        .get_template(fl)
        .render(**o)
    )


try:
    import dotenv

    dotenv.load_dotenv(".env.production")
except:
    pass

LINKS = [
    ["/", "weekly", "1"],
]  # All the routes currently the site has

DATA = json.loads(read("./src/langs/locales.json"))
DEFAULT_LOCALE = DATA["default_locale"]
LOCALES = DATA["locales"]


def make_sitemap():
    ROOT = os.getenv("PUBLIC_SITE_URL") or ""
    SITEMAP_LINKS = []
    for lnk in LINKS:
        lnk[0] = ROOT + (lnk[0] if lnk[0] != "/" else "")
        SITEMAP_LINKS.append(lnk)
        for lcl in LOCALES:
            if lcl == DEFAULT_LOCALE:
                continue
            link = lnk.copy()
            link[0] += f"/{lcl}"
            SITEMAP_LINKS.append(link)

    write("dist/sitemap.xml", render("sitemap.xml", SITEMAP_LINKS=SITEMAP_LINKS))
    write("dist/robots.txt", render("robots.txt", SITE_URL=ROOT))


def migrate_routes():
    """This is to Migrate routes like `bn/index.html` -> `bn.html`"""
    ROOT = "dist"
    for t in LINKS:
        x = t[0]
        for lcl in LOCALES:
            nm = f"{ROOT}/{lcl+x}"
            pth = f'{nm+("/" if x!="/" else "")}index.html'
            if nm[-1] == "/":
                nm = nm[:-1]
            write(f"{nm}.html", read(pth))
            os.remove(pth)
            if len(os.listdir(nm)) == 0:
                delete_folder(nm)


migrate_routes()
make_sitemap()
