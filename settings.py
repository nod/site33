from os import path

# tornado specific
settings = dict(

    users = {},

    blog_admin = None,
    dbposts = None,  # BAD! Stores in MEMORY
    dbpaste = None,  # BAD! Stores in MEMORY
    dbpages = None,  # BAD! Stores in MEMORY

    port = 6488,
    login_url="/auth",
    static_path = path.join(path.dirname(__file__), "static"),
    template_path = path.join(path.dirname(__file__), "templates"),
    cookie_secret = None, # set in settings_local.settings

    debug = False,
    debug_pdb = False,

    twitter_admins = [],
    twitter_consumer_secret = None,
    twitter_consumer_key = None,
    twitter_cb_uri = 'http://localhost:6488/auth/twitter',
    )

try:
    from settings_local import settings as sl
    settings.update(sl)
except:
    pass
