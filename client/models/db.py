# -*- coding: utf-8 -*-

# -------------------------------------------------------------------------
# AppConfig configuration made easy. Look inside private/appconfig.ini
# Auth is for authenticaiton and access control
# -------------------------------------------------------------------------
from gluon.contrib.appconfig import AppConfig
from gluon.tools import Auth

# -------------------------------------------------------------------------
# This scaffolding model makes your app work on Google App Engine too
# File is released under public domain and you can use without limitations
# -------------------------------------------------------------------------

if request.global_settings.web2py_version < "2.15.5":
    raise HTTP(500, "Requires web2py 2.15.5 or newer")

# -------------------------------------------------------------------------
# if SSL/HTTPS is properly configured and you want all HTTP requests to
# be redirected to HTTPS, uncomment the line below:
# -------------------------------------------------------------------------
# request.requires_https()

# -------------------------------------------------------------------------
# once in production, remove reload=True to gain full speed
# -------------------------------------------------------------------------
configuration = AppConfig(reload=True)

if not request.env.web2py_runtime_gae:
    # ---------------------------------------------------------------------
    # if NOT running on Google App Engine use SQLite or other DB
    # ---------------------------------------------------------------------
    db = DAL(configuration.get('db.uri'),
             pool_size=configuration.get('db.pool_size'),
             migrate_enabled=configuration.get('db.migrate'),
             check_reserved=['all'])
else:
    # ---------------------------------------------------------------------
    # connect to Google BigTable (optional 'google:datastore://namespace')
    # ---------------------------------------------------------------------
    db = DAL('google:datastore+ndb')
    # ---------------------------------------------------------------------
    # store sessions and tickets there
    # ---------------------------------------------------------------------
    session.connect(request, response, db=db)
    # ---------------------------------------------------------------------
    # or store session in Memcache, Redis, etc.
    # from gluon.contrib.memdb import MEMDB
    # from google.appengine.api.memcache import Client
    # session.connect(request, response, db = MEMDB(Client()))
    # ---------------------------------------------------------------------

# -------------------------------------------------------------------------
# by default give a view/generic.extension to all actions from localhost
# none otherwise. a pattern can be 'controller/function.extension'
# -------------------------------------------------------------------------
response.generic_patterns = [] 
if request.is_local and not configuration.get('app.production'):
    response.generic_patterns.append('*')

# -------------------------------------------------------------------------
# choose a style for forms
# -------------------------------------------------------------------------
response.formstyle = 'bootstrap4_inline'
response.form_label_separator = ''

# -------------------------------------------------------------------------
# (optional) optimize handling of static files
# -------------------------------------------------------------------------
# response.optimize_css = 'concat,minify,inline'
# response.optimize_js = 'concat,minify,inline'

# -------------------------------------------------------------------------
# (optional) static assets folder versioning
# -------------------------------------------------------------------------
# response.static_version = '0.0.0'

# -------------------------------------------------------------------------
# Here is sample code if you need for
# - email capabilities
# - authentication (registration, login, logout, ... )
# - authorization (role based authorization)
# - services (xml, csv, json, xmlrpc, jsonrpc, amf, rss)
# - old style crud actions
# (more options discussed in gluon/tools.py)
# -------------------------------------------------------------------------

# host names must be a list of allowed host names (glob syntax allowed)
auth = Auth(db, host_names=configuration.get('host.names'))

# -------------------------------------------------------------------------
# create all tables needed by auth, maybe add a list of extra fields
# -------------------------------------------------------------------------
auth.settings.extra_fields['auth_user'] = []
auth.define_tables(username=False, signature=False)

# -------------------------------------------------------------------------
# configure email
# -------------------------------------------------------------------------
mail = auth.settings.mailer
mail.settings.server = 'logging' if request.is_local else configuration.get('smtp.server')
mail.settings.sender = configuration.get('smtp.sender')
mail.settings.login = configuration.get('smtp.login')
mail.settings.tls = configuration.get('smtp.tls') or False
mail.settings.ssl = configuration.get('smtp.ssl') or False

# -------------------------------------------------------------------------
# configure auth policy
# -------------------------------------------------------------------------
auth.settings.registration_requires_verification = False
auth.settings.registration_requires_approval = False
auth.settings.reset_password_requires_verification = True

# -------------------------------------------------------------------------  
# read more at http://dev.w3.org/html5/markup/meta.name.html               
# -------------------------------------------------------------------------
response.meta.author = configuration.get('app.author')
response.meta.description = configuration.get('app.description')
response.meta.keywords = configuration.get('app.keywords')
response.meta.generator = configuration.get('app.generator')
response.show_toolbar = configuration.get('app.toolbar')

# -------------------------------------------------------------------------
# your http://google.com/analytics id                                      
# -------------------------------------------------------------------------
response.google_analytics_id = configuration.get('google.analytics_id')

# -------------------------------------------------------------------------
# maybe use the scheduler
# -------------------------------------------------------------------------
if configuration.get('scheduler.enabled'):
    from gluon.scheduler import Scheduler
    scheduler = Scheduler(db, heartbeat=configuration.get('scheduler.heartbeat'))

# -------------------------------------------------------------------------
# Define your tables below (or better in another model file) for example
#
# >>> db.define_table('mytable', Field('myfield', 'string'))
#
# Fields can be 'string','text','password','integer','double','boolean'
#       'date','time','datetime','blob','upload', 'reference TABLENAME'
# There is an implicit 'id integer autoincrement' field
# Consult manual for more options, validators, etc.
#
# More API examples for controllers:
#
# >>> db.mytable.insert(myfield='value')
# >>> rows = db(db.mytable.myfield == 'value').select(db.mytable.ALL)
# >>> for row in rows: print row.id, row.myfield
# -------------------------------------------------------------------------

# -------------------------------------------------------------------------
# after defining tables, uncomment below to enable auditing
# -------------------------------------------------------------------------
# auth.enable_record_versioning(db)


db.define_table('rn220systems',
                Field('SerialNo',         'string'  ),
                Field('IP',               'string'  ),
                Field('VPNIP',            'string'  ),
                Field('WANIP',            'string'  ),
                Field('PORT',             'integer' ),
                Field('devCycle',         'integer', rname='Cycle'),
                Field('AutoSet',          'integer' ),
                Field('Status',           'integer' ),
                Field('devLocation',      'string', rname='Location'),
                Field('Place',            'string'  ),
                Field('devState',         'string', rname='State'),
                Field('TimeOut',          'integer' ),
                Field('CommFail',         'integer' ),
                Field('Latitude',         'double'  ),
                Field('Longitude',        'double'  ),
                Field('Altitude',         'double'  ),
                Field('InstallationDate', 'datetime'),
                Field('StationID',        'integer' ),
                Field('RadonGradient',    'integer' ),
                Field('RadonExhalation',  'integer' ),
                Field('BSNLMobNo',        'string'  ),
                Field('SiteContactNo',    'string'  ),
                Field('PersonInCharge',   'string'  ),
                Field('SeismicZone',      'integer' ),
                Field('devMode',          'string', rname='Mode'),
                Field('PumpAction',       'integer' ),
                Field('PumpOntime',       'integer' ),
                Field('PumpOfftime',      'integer' ),
                Field('GroupID',          'integer' ),
                primarykey=['SerialNo'],
                migrate=True
               )


db.define_table('rndata',
                Field('Pointer',          'integer' ),
                Field('SlNo',             'integer' ),
                Field('SerialNo',         'string'  ),
                Field('devMode',          'string', rname='Mode'),
                Field('devCycle',         'integer', rname='Cycle'),
                Field('Datetime',             'datetime', rname='TimeStamp'),
                Field('Counts',           'integer' ),
                Field('BGCounts',         'integer' ),
                Field('Concentration',    'integer' ),
                Field('Sigma',            'double'  ),
                Field('Temperature',      'double'  ),
                Field('Humidity',         'double'  ),
                Field('BattVoltage',      'double'  ),
                Field('PMTVoltage',       'double'  ),
                Field('Pressure',         'double'  ),
                #primarykey=['Pointer', 'SerialNo', 'Datetime'],
                migrate=True
               )



#db.auth_user.truncate()
#db.commit()
if not (db(db.auth_user.id>0).select()):
    db.auth_user.update_or_insert(db.auth_user.email=='indra@barc.gov.in',
                                  first_name='Indra',
                                  last_name='User',
                                  email='indra@barc.gov.in',
                                  password='pbkdf2(1000,20,sha512)$9efc00dbc65c4a4f$7e46fc0551f344bced53f9b5c4e3896c403011c1')
    db.commit()

#db.rndata.truncate()
#db.commit()
