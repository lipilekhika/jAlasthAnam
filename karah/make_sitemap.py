import json, jinja2, os, shutil, sys


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

    def normalise_url(url: str):
        return url if url != "/" else ""

    for lnk in LINKS:
        url_part = normalise_url(lnk[0])
        for lcl in LOCALES:
            link = lnk.copy()
            if lcl == DEFAULT_LOCALE:
                link[0] = ROOT + url_part
            else:
                link[0] = f"{ROOT}/{lcl+url_part}"
            SITEMAP_LINKS.append(link)

    write("dist/sitemap.xml", render("sitemap.xml", SITEMAP_LINKS=SITEMAP_LINKS))
    write("dist/robots.txt", render("robots.txt", SITE_URL=ROOT))


def migrate_routes():
    """This is to Migrate routes like `bn/index.html` -> `bn.html` and `drive/index.html` -> `drive.html`"""

    def normalise_html_file_location(nm: str):
        pth = f'{nm+("/" if x!="/" else "")}index.html'
        if nm[-1] == "/":
            nm = nm[:-1]
        write(f"{nm}.html", read(pth))
        os.remove(pth)
        if len(os.listdir(nm)) == 0:
            delete_folder(nm)

    ROOT = "dist"
    for t in LINKS:
        x = t[0]
        for lcl in LOCALES:
            nm = f"{ROOT}/{lcl+x}"
            normalise_html_file_location(nm)
            if lcl == DEFAULT_LOCALE and x != "/":
                # to normalize files like `drive/index.html` -> drive.html
                normalise_html_file_location(ROOT + x)


if sys.argv[-1] != "no-migrate":
    migrate_routes()
make_sitemap()
