# -*- coding: utf-8 -*-
import uuid, os 


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
configuration = AppConfig()

if not request.env.web2py_runtime_gae:
    # ---------------------------------------------------------------------
    # if NOT running on Google App Engine use SQLite or other DB
    # ---------------------------------------------------------------------
    db = DAL(configuration.get('db.uri'),
             pool_size=configuration.get('db.pool_size'),
             migrate_enabled=configuration.get('db.migrate'),
             fake_migrate=configuration.get('db.fake_migrate'),
             lazy_tables=True,
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
# ENUMS
# -------------------------------------------------------------------------

# registration status
USER_STATUS_ID = {-2: T('BLOCKED'), -1: T('DISAPPROVED'), 1: T('EMAIL UNVERFIED'), 2:T('EMAIL VERIFIED'), 3:T('ACTIVATED')}

USER_STATUS_ID_ACTION = {
    1: {2: T('VERIFY EMAIL'), 3: T('ACTIVATE')},
    2: {3: T('ACTIVATE'), -1: T('DEACTIVATE'), -2: T('BLOCK')},
    3: {-1: T('DEACTIVATE'), -2: T('BLOCK')},
    -2: {3: T('ACTIVATE')},
}



COMMENT_TYPE = {
    0: 'Read',
    1: 'Write' #read and write
}

COLOR = {
    1: T('Red'),
    2: T('Green'),
    3: T('Orange'),
    4: T('Blue'),
} 

PRIORITY = {
    0: T('Emergency'),
    1: T('Urgent'),
    2: T('Normal'),
    3: T('None'),
    # 5: T('Attention'),
}

TAG_TYPE = {
    0: T('Todo'),
    1: T('Label'),
}

TAG_STATUS = {
    0: T('In Progress'),
    1: T('Complete'),
    2: T('Browse'),
}

SORT_TYPE = {
    0 : T('By Date and Time'),
    1 : T('Urgency'),
    2 : T('By Name')
}

ORDER_TYPE = {
    0 : T('Ascending'),
    1 : T('Descending')
}

SORT_CONDITION = {
    0 : T('Show all tags'),
    1 : T('Address yourself'),
    2 : T('Emergency Tags Only'),
    3 : T('Complete tags only')
}

MINIMAP_ROTATION = {
    0 : T('Normal'),
    1 : T('90 Degrees'),
    2 : T('180 Degrees'),
    3 : T('270 Degrees')
}



# -------------------------------------------------------------------------
# create all tables needed by auth, maybe add a list of extra fields
# -------------------------------------------------------------------------
auth.settings.extra_fields['auth_user'] = [
    Field('company_name','string',length=254),
    Field('space_license','integer',length=3,comment=T('space licenses')),
    Field('mobile','string',length=32,requires=IS_EMPTY_OR(IS_MATCH('^[0-9]{10}$',error_message=T('invalid phone number'))), comment='(ex: 9171234567)'),
    Field('phone','string',length=32,requires=IS_EMPTY_OR(IS_MATCH('^[0-9]{10}$',error_message=T('invalid phone number'))), comment='(ex: 9171234567)'),
    # Field('birthdate','date',requires=IS_EMPTY_OR(IS_DATE(format=T('%Y-%m-%d'),error_message=T('must be in YYYY-MM-DD')))),
    Field('status_id','string',length=16,requires=IS_EMPTY_OR(IS_IN_SET(USER_STATUS_ID)),required=False, label='Status',hidden=True,readable=False,writable=True),

    Field('uuid',length=64,default=str(uuid.uuid4()).upper(), hidden=True,readable=True,writable=True),
]


auth.define_tables(username=False, signature=False)

# -------------------------------------------------------------------------
# configure email
# -------------------------------------------------------------------------
mail = auth.settings.mailer
mail.settings.server = configuration.get('smtp.server')
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


# IMPORTANT: These common fields are added automatically to each define tables (yes)
db._common_fields = [   

    Field('created_on','datetime',default=request.now,label=T('<created>'),writable=False,readable=False),
    Field('modified_on','datetime',update=request.now,label=T('<modified>'),writable=False,readable=False),

    Field('created_by','integer',default=auth.user.id if auth.user else None,label=T('<by>'),writable=False,readable=False),
    Field('modified_by','integer',update=auth.user.id if auth.user else None,label=T('<by>'),writable=False,readable=False),

    Field('ip','string',default=request.client,update=request.client,compute=lambda row: request.client,label=T('<ip>'),writable=False,readable=False),
    Field('user_agent','string',default=request.user_agent(),update=request.user_agent(),compute=lambda row: request.user_agent(),
        writable=False,readable=False,label=T('<device>'))
]

# =====> USING UUID AS PRIMARY KEY <=====
# making sure all children of parent will have same UUID
# db.person.uuid.default = db.thing.uuid.default = lambda:str(uuid.uuid4())

# db.thing.owner_id.requires = IS_IN_DB(db, 'person.uuid', '%(name)s')

# usage example
# if db(db.person).isempty():
#     nid = str(uuid.uuid4())
#     db.person.insert(uuid=nid, name='Massimo')
#     db.thing.insert(name='Chair', owner_id=nid)
# =====> USING UUID AS PRIMARY KEY <=====

# ====> WE ARE USING PLURAL TABLES NAMES <=====


# -------------------------------------------------------------------------
# APSI SECURITY
# -------------------------------------------------------------------------
db.define_table('api_security',
    Field('client_name','string',length=128,required=True,label=T('Client Name')),
    Field('email_address','string',required = False,length=64,label=T('Email Address')),
    Field('phone', required = False, label=T('Phone Number')),
    Field('client_domain','string',length=128,required=True),
    Field('client_secret','string',length=128,required=False),
    Field('api_key','string',default=str(uuid.uuid4()),length=128),
    Field('signature','string',length=128,required=False),
    Field('expiry','datetime'),
    Field('requests','string',length=128,required=False),
)


# -------------------------------------------------------------------------
# LAYERS
# -------------------------------------------------------------------------
db.define_table('layers',
    Field('uuid',length=64,default=str(uuid.uuid4()).upper(), hidden=True,readable=True,writable=True),
    Field('layer_name','string',length=100,requires=IS_NOT_EMPTY(),required=True,label=T('Layer Name')),
    # Field('layer_type_id','integer',requires=IS_NOT_EMPTY(),default=0,required=True,label=T('Layer Type')),
    Field('parent_uuid','string',length=64), # parent layer id
    
    primarykey=['uuid'],
 )

# -------------------------------------------------------------------------
# SPACES
# -------------------------------------------------------------------------
db.define_table('spaces', #space is reserved word
    Field('uuid',length=64,default=str(uuid.uuid4()).upper(), hidden=True,readable=True,writable=True),
    Field('layer_uuid','references layers',requires=IS_IN_DB(db,'layers.uuid','%(layer_name)s'.capitalize()),required=True,label=T('Layer')),
  
    # space detail
    Field('space_sid','string',length=100,requires=IS_NOT_EMPTY(),required=True,unique=True,label=T('SID')), #matterport space uid
    Field('space_name','string',length=128,requires=IS_NOT_EMPTY(),required=True,label=T('Space Name')),
    Field('space_url','string',length=124,requires=IS_NOT_EMPTY(),required=True,label=T('Space URL')),

    # cover image
    Field('space_image','upload',uploadfolder=os.path.join(request.folder, 'static', 'uploads'),label=T('Space Image')),
    Field('minimap_image','upload',uploadfolder=os.path.join(request.folder, 'static', 'uploads'),label=T('Minimap Image')),

    Field('minimap_rotation','integer',requires=IS_IN_SET(MINIMAP_ROTATION),default=0,label=T('Minimap Rotation')),
    Field('csv_import','upload',uploadfolder=os.path.join(request.folder, 'static', 'uploads'),label=T('CSV Import')),

    Field('client_name','string',length=100,label=T('Client Name')),
    Field('space_user_id','integer',requires=IS_EMPTY_OR(IS_IN_DB(db,'auth_user.id','%(first_name)s' )),required=False,label=T('SpaceIncharge')), 
    Field('site_user_id','integer',requires=IS_EMPTY_OR(IS_IN_DB(db,'auth_user.id','%(first_name)s' )),required=False,label=T('Site Incharge')), 

    Field('memo1','string',length=1024,label=T('Memo 1')),
    Field('memo2','string',length=1024,label=T('Memo 2')),
    
    primarykey=['uuid'],
 )

# -------------------------------------------------------------------------
# EVENTS
# -------------------------------------------------------------------------
db.define_table('events', #event is reserved word
    Field('uuid',length=64,default=str(uuid.uuid4()).upper(), hidden=True,readable=True,writable=True),
    Field('space_uuid','references spaces',requires=IS_IN_DB(db,'spaces.uuid','%(space_name)s'.capitalize()),required=True,label=T('Space')),
    Field('event_name','string',length=256,requires=IS_NOT_EMPTY(),required=True,label=T('Event Name')),

    primarykey=['uuid'],
)


# -------------------------------------------------------------------------
# 3D objects/media table
# -------------------------------------------------------------------------
db.define_table('media',
    Field('upload_file','upload',uploadfolder=os.path.join(request.folder, 'api', 'uploads')),
    Field('upload_filename','string',length=128,label=T('Filename')),
    Field('filename','string',length=128,label=T('Filename')),
    Field('uuid',length=64,default=str(uuid.uuid4()).upper(), hidden=True,readable=True,writable=True),
    Field('name','string',length=128,label=T('Name'),requires=IS_NOT_EMPTY(),required=True),
    Field('description','text',label=T('Description')), 
    Field('object_label', 'text',length=128, label="Label",requires=IS_NOT_EMPTY(),required=True), #comma separated values, tags — text, for search like “sofa”
    Field('object_type','text',default='',length=32768,label=T('3D Type'),requires=IS_NOT_EMPTY(),required=True),
    Field('object_key','string',length=64,default=str(uuid.uuid4()),label=T('Key')),
    Field('amazon_uri','string',length=512,label=T('URI')),
    primarykey=['uuid'],
)



