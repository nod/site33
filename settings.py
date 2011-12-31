from os import path

# tornado specific
settings = dict(
    dbposts = '',  # BAD IN MEMORY
    dbmeta = '',  # BAD IN MEMORY
    dbpaste = '',  # BAD IN MEMORY
    port = 6488,
    login_url="/auth/login",
    static_path = path.join(path.dirname(__file__), "app33/static"),
    template_path = path.join(path.dirname(__file__), "app33/templates"),
    cookie_secret = None, # set in settings_local.settings
    debug = False,
    debug_pdb = False,
    )

try:
    from settings_local import settings as sl
    settings.update(sl)
except:
    pass
