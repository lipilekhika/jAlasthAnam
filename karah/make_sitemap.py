import json, jinja2, os, shutil, sys


def write(loc: str, val: str):
    f = open(loc, encoding="utf-8", mode="w")
    f.write(val)
    f.close()


def read(loc: str):
    f = open(loc, encoding="utf-8", mode="r")
    vl = f.read()
    f.close()
    return vl


def render(fl: str, **o):
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
    ROOT_URL = os.getenv("PUBLIC_SITE_URL") or ""
    SITEMAP_LINKS = []

    def normalise_url(url: str):
        return url if url != "/" else ""

    for lnk in LINKS:
        url_part = normalise_url(lnk[0])
        for lcl in LOCALES:
            link = lnk.copy()
            if lcl == DEFAULT_LOCALE:
                link[0] = ROOT_URL + url_part
            else:
                link[0] = f"{ROOT_URL}/{lcl+url_part}"
            SITEMAP_LINKS.append(link)

    TEMPLATES = {
        "dist/sitemap.xml": ["sitemap.xml.j2", dict(SITEMAP_LINKS=SITEMAP_LINKS)],
        "dist/robots.txt": ["robots.txt.j2", dict(SITE_URL=ROOT_URL)],
        "dist/_redirects": ["_redirects.j2", dict(DEFAULT_LOCALE=DEFAULT_LOCALE)],
    }
    for fl in TEMPLATES:
        tmp: str = TEMPLATES[fl][0]
        data = TEMPLATES[fl][1]
        write(fl, render(tmp, **data))


def migrate_routes():
    """This is to Migrate routes like `bn/index.html` -> `bn.html` and `drive/index.html` -> `drive.html`"""

    def normalise_html_file_location(nm: str):
        pth = f'{nm+("/" if x!="/" else "")}index.html'
        if nm[-1] == "/":
            nm = nm[:-1]
        shutil.copyfile(pth, f"{nm}.html")
        os.remove(pth)
        if len(os.listdir(nm)) == 0:
            shutil.rmtree(nm)

    ROOT_DIR = "dist"
    for t in LINKS:
        x = t[0]
        for lcl in LOCALES:
            if lcl != DEFAULT_LOCALE:
                nm = f"{ROOT_DIR}/{lcl+x}"
                normalise_html_file_location(nm)
            elif lcl == DEFAULT_LOCALE and x != "/":
                # to normalize files like `drive/index.html` -> drive.html
                normalise_html_file_location(ROOT_DIR + x)


if sys.argv[-1] != "no-migrate":
    migrate_routes()
make_sitemap()
