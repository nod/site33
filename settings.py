from os import path

# tornado specific
torn_settings = dict(
    dbposts = '/tmp/blog.tokyo',
    dbmeta = '/tmp/blogmeta.tokyo',
    port = 6488,
    db_name = "",
    db_uri  = "",
    db_user = "",
    db_pass = "",
    login_url="/auth/login",
    static_path = path.join(path.dirname(__file__), "app33/static"),
    template_path = path.join(path.dirname(__file__), "app33/templates"),
    cookie_secret = "SOMETHING HERE",
    debug = False,
    debug_pdb = False,
)
try:
    from settings_prod import torn_settings as ts
except:
    from settings_dev import torn_settings as ts
torn_settings.update(ts)

