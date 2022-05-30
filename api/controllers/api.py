from treelib import Node, Tree
import json

response.view = 'generic.json' 

response.headers['Content-Type'] = 'application/json; charset=utf-8'
response.headers['Access-Control-Allow-Origin'] = 'locahost:8888'
response.headers['Access-Control-Max-Age'] = 86400
response.headers['Access-Control-Allow-Headers'] = 'Origin'
response.headers['Access-Control-Allow-Methods'] = ['GET','POST','PUT','OPTIONS']
response.headers['Access-Control-Allow-Credentials'] = 'true'
response.headers['Access-Control-Allow-Headers'] = "Accept, Authorization, Content-Type, If-Match, If-Modified-Since, If-None-Match, If-Unmodified-Since, Accept-Encoding"



def valid_api_key(app_key=None):
    # do check if the api_key exist in the api_sec table if yes return true, else false
    if app_key==None:
        if request.env.HTTP_APPKEY:
            app_key = request.env.HTTP_APPKEY
        elif request.env.HTTP_AUTHORIZATION:
            app_key = request.env.HTTP_AUTHORIZATION
        else:
            return False
    
    domain=request.env.HTTP_HOST

    aps = db.api_security
    query = aps.api_key == app_key
    query &= aps.client_domain.contains(domain)
    result = db(query).count()

    
    logger.info("--> API REQUEST: {0}, {1}, {2}".format(app_key,domain,result))

    if result:
        return True
    else: 
        logger.warning('====> WARNING: INVALID API_KEY REQUESTED <=== {0}, {1}'.format(domain,app_key))
        return False

@request.restful()
def v1():
    response.view = 'generic.json' 

    # allow CORS

    response.headers['Access-Control-Allow-Origin'] = 'localhost:8888'
    response.headers['Access-Control-Allow-Methods'] = "POST,GET,OPTIONS,PUT"
    response.headers['Access-Control-Allow-Credentials'] = "true"
    response.headers['Access-Control-Allow-Headers'] = "Accept, Authorization, Content-Type, If-Match, If-Modified-Since, If-None-Match, If-Unmodified-Since, Accept-Encoding"

    # @auth.requires(valid_api_key(), requires_login=False)   
    # @auth.requires_login()
    def GET(*args, **vars):  
        response.view = 'generic.json' 
        logger.info('args: {0} , vars: {1}'.format(args,vars))

        if len(args)<=0:
            return 'no matching pattern'

        # table_name
        if len(args)==1 and args[0] in [*db.tables,'users','trees']: 
            table_name = args[0]

            # TREES OF LAYERS / FOLDERS
            if table_name == 'trees':
                ly = db.layers
                tree = Tree()
                layers = db(ly).select(ly.uuid,ly.parent_uuid,ly.layer_name).as_dict(key='uuid')
                while len(layers):
                    for k,v in list(layers.items()):
                        if not v['parent_uuid']: 
                            if not tree.root:
                                tree.create_node(tag=v['layer_name'],identifier=k,data=v)
                                layers.pop(k)
                        else:
                            if tree.contains(v['parent_uuid']) and not tree.contains(k): 
                                tree.create_node(tag=v['layer_name'],identifier=k,parent=v['parent_uuid'],data=v)
                                layers.pop(k)

                    res = json.loads(tree.to_json(with_data=True))
                    logger.info(tree.all_nodes())

                    return dict(data = res)

            # WARNING!!!
            if table_name == 'users':
                logger.info('WARNING!!! This returns ALL users...')
                table_name = 'auth_user'
                t = db[table_name]
                return dict(data=db(t).select(t.uuid,t.first_name,t.last_name,t.email,t.mobile,t.phone,t.company_name,t.space_license,t.status_id,cache=(cache.ram, 5), cacheable=True))

            t = db[table_name]
            return dict(data=db(t).select(t.ALL,cache=(cache.ram, 5), cacheable=True))

        # table_name/[uuid]
        if len(args)==2 and args[0] in [*db.tables,'users']: 

            table_name = args[0]
            if table_name == 'users':
                table_name = 'auth_user'

            t = db[table_name]
            c = 'uuid'
            return dict(data=db(t[c] == args[1]).select(t.ALL,cache=(cache.ram,5), cacheable=True))

        # table_name/column/value
        if len(args)==3 and  args[0] in [*db.tables,'users']: 
            table_name = args[0]
            
            # WARNING!!!
            if table_name == 'users':
                table_name = 'auth_user'

            t = db[table_name]
            c = args[1].replace('-','_')
            return dict(data=db(t[c] == args[2]).select(t.ALL,cache=(cache.ram, 5), cacheable=True))
        else:
            return 'no matching pattern'

        return locals()
   
    # @auth.requires(valid_api_key(), requires_login=False)
    # @auth.requires_login()
    def POST(table_name, **vars):
        response.view = 'generic.json' 
        logger.info('table: {0} , vars: {1}'.format(table_name,vars))

        # make sure uuid is not set to enable db default
        if 'uuid' in vars: vars.pop('uuid')

        if table_name not in [*db.tables,'users']:
            return 'no matching pattern'

        if table_name == 'users': table_name = 'auth_user'
        # extract table
        t = db[table_name]

        # try insert
        res = t.validate_and_insert(**vars)
       

        if not res.errors:
            data = db(t.uuid == res.id['uuid']).select(t.ALL).first().as_dict()
            return dict(data=data)
        else:
            res.pop('id')
            return dict(res)

    # @auth.requires(valid_api_key(), requires_login=False)   
    # @auth.requires_login()
    def PUT(*args, **vars):
        response.view = 'generic.json' 
        logger.info('args: {0} ,  vars: {1}'.format(args,vars))

        # force remove uuid to avoid overriding 
        # if 'uuid' in vars: vars.pop('uuid')

        # verify parameters
        if len(args)<2 or vars == {}:
            return 'no matching pattern'

        if args[0] in [*db.tables,'users']:
            table_name = args[0]
            uuid = args[1]
        else:
            return 'no matching pattern'


        if table_name == 'users': table_name = 'auth_user'

        # extract table and id
        t = db[table_name]    

        logger.info('PUT... {0}, {1}, {2}'.format(t,uuid,vars))

        # try update
        res = db(t.uuid==uuid).update(**vars)

        logger.info('result: {}'.format(res))



        # include updated data in response
        if res == 1:
            data = db(t.uuid == uuid).select(t.ALL).first()
            return dict(data=data)
        else:
            return dict(res)

    # @auth.requires_login()
    def DELETE(table_name, uuid, *args):
        response.view = 'generic.json' 
        logger.info('table: {0} , uuid: {1}, args: {2}'.format(table_name,uuid,args))

        # extract table and id
        if table_name in [*db.tables,'users']:
            if table_name == 'users': table_name = 'auth_user'
            t = db[table_name]
        else:
            return 'no matching pattern'

        # try delete
        res = db(t.uuid==uuid).delete()
        logger.info('res: {}'.format(res))
        

        return dict(deleted=res,errors={})

    # don't remove the line below
    return locals()

@request.restful()
def cas(): 
    '''
    CAS REST protocol

    api/cas/validate
    api/cas/tickets
    api/cas/users

    '''

    def GET(*args, **vars):
        logger.info('GET CAS() args: {0}, vars: {1}'.format(args,vars))
        response.view ='generic.json'
        

        # short alias
        u = db.auth_user
        m = db.auth_membership

        # ===> VALIDATE TICKET <====
        if 'validate' in args[0]:
            '''
            GET /api/cas/validate/<ticket>

            - to validate authentication ticket

            params:
            - ticket        Authentication ticket previously issued by this CAS
            
            '''

            logger.info('auth: {}'.format(session))

            if len(args)<2:
                return dict(status='fail',message='missing parameters')

            ticket = args[1]
            
            result = db(db.auth_cas.ticket==ticket).select(db.auth_cas.ALL).first()
            logger.info('result: {}'.format(result))

            if result !=None:
                # response.code=200
                logger.info(result.user_id)
                user_uuid = db(db.auth_user.id == result.user_id).select(db.auth_user.uuid).first()['uuid']
                logger.info(user_uuid)
                
                result.update(dict(uuid=user_uuid))
                return dict(status="success",data=session)
            else:
                return dict(status="fail",message="invalid ticket")

        # response.code = 400
        return dict(status="fail")

    def POST(*args,**vars):
        logger.info('args: {0}, vars: {1}'.format(args,vars))
        response.view = 'generic.json'

        # ===> REGISTER / CREATE USER <===
        if len(args)>0 and args[0] in ['users']:
            '''
            POST /api/cas/users
            - create or register User

            params:
            - first_name        Firstname of user
            - last_name         Lastname of user
            - email             Email address
            - password          Password
            '''

            logger.info('REGISTER USER ==> args: {0}, vars: {1}'.format(args,vars))

            if not vars: return dict(status="fail",message="missing parameters")

            # first_name and last_name is required, so set some value
            if not('first_name' in vars) and ('fullname' in vars):
                vars['first_name'] = vars['fullname'].split(' ')[0]
                vars['last_name'] = vars['fullname'].split(' ')[-1]

            # force remove id since this is create
            if 'id' in vars: vars.pop('id')

            result = db.auth_user.validate_and_insert(**vars)
            logger.info('result: {}'.format(result))

            if result['errors']:
                return dict(status="error",errors=result['errors'])
            else:   
                user = db.auth_user[result.id]              
                return dict(status="success",data=user)

        # ====> CREATE ACCESS TICKET (AUTHENTICATE) <=== 
        if 'tickets' in args[0]:
            '''

            POST api/cas/tickets
            - authenticates User

            params:
                - email         Email of user
                - password      Password of user

            return:
                - ticket        Access ticket
                - data          Includes user and session detail
            
            '''

            # validate parameters
            if vars == {}: return dict(status='fail',message="missing parameters")
            if not( 'email' in vars and 'password' in vars): return dict(status='fail',message="missing parameters")

            # force clear ticket
            auth.user = None

            # check if user is still in session
            if (auth.user == None) or (auth.user and auth.user.email != vars['email']):
                # attempt to login
                user = auth.login_bare(vars['email'].strip(),vars['password'].strip())
                logger.info('user: {}'.format(user))
                logger.info('auth.user: {}'.format(auth.user))
                if not user:
                    return dict(status='fail', message="invalid user credentials")
                
                logger.info('session: {}'.format(session))

            if auth.user:
                ticket = 'ST-1-{0}'.format(session.auth.hmac_key)
                db.auth_cas.update_or_insert(ticket==ticket,user_id=session.auth.user.id,ticket=ticket)

                data = session
                data.update(ticket=ticket)

                return dict(status='success',data=data)

        # response.code = 404
        return dict(status="error")

    def PUT(*args,**vars):
        logger.info('args: {0}, vars: {1}'.format(request.args,request.vars))
        response.view = 'generic.json'

        # update user
        if len(args)>0 and args[0] in ['users']:
            # get record uuid
            user_uuid = int(args[1] or 0)
            if not user_uuid:
                logger.info('{}'.format(uuid))
                return dict(status="fail",message='uuid is required')

            # first_name and last_name is required, so update it too
            if not('first_name' in vars) and ('fullname' in vars):
                logger.info('{}'.format(record_id))
                vars['first_name'] = vars['fullname'].split(' ')[0]
                vars['last_name'] = vars['fullname'].split(' ')[-1]
 
            if user_uuid:
                try:
                    result = db(db.auth_user.uuid==user_uuid).validate_and_update(**vars)
                    return dict(status="success",data=result)
                except:
                    return dict(status="error",error=T('Server or database error.'))
        
        # update membership role
        if len(args)>0 and args[0] in ['memberships']:

            # get record id 
            record_id = int(args[1] or 0)
            if record_id == 0:
                logger.info('{}'.format(record_id))
                return dict(status="fail",message='record id is required')
 
            if record_id>0:
                try:
                    result = db(db.auth_membership.user_id==record_id).validate_and_update(**vars)
                    return dict(status="success",data=result)
                except:
                    return dict(status="error",error=T('Server or database error.'))

        return dict(status="error")

    def DELETE(*args):
        logger.info('args: {0}, vars: {1}'.format(request.args,request.vars))
        response.view ='generic.json'
        
        if 'tickets' in args[0]:
            ticket = args[1]
            result = db(db.auth_cas.ticket==ticket).delete()
            if result != None: session = None

            logger.info('session: {}'.format(session))

            return dict(status="success")
        
        if 'users' in args[0]:
            user_id = int(args[1])
            result = db(db.auth_user.id==user_id).delete()
            logger.info('result: {}'.format(result))
            if result != None: session = None

            logger.info('session: {}'.format(session))

            # response.code=200
            return dict(status="success")
    
        if 'membership' in args[0]:
            user_id = int(args[1])
            result = db(db.auth_membership.user_id==user_id).delete()
            logger.info('result: {}'.format(result))
            if result != None: session = None

            logger.info('session: {}'.format(session))

            # response.code=200
            return dict(status="success")

        # response.code = 404
        return dict(status="error")

    return locals() #do not remove this


@request.restful()
def s3():

    def GET(*args, **vars):
        response.view='generic.json'
        
        logger.info('request.args {0}'.format(request.args))
        if request.args(0) == 'file':
            # get 1 object in amazon s3 and server via object id
            if request.args(1) == 'uuid':
                uuid = int(request.args(2) or 0)
                query_result = db(db.media.uuid == uuid).select()
                
                data_objects = []
                for qr in query_result:
                    logger.info('QUERY RESULT {0}'.format(qr))
                    amazon_key = qr.object_key + '.' + qr.object_type
                    isExist = get_object(amazon_key)
                    # append if object_key exists in amazon s3
                    if isExist['isExist'] == True:
                        data_objects.append(qr)

                return dict(status='success',data=data_objects)
            # get 1 object in amazon s3 and server via user-uuid
            elif request.args(1) == 'user-uuid':
                user_uuid = request.args(2)
                query_result = db(db.media.uuid == user_uuid).select()
                
                data_objects = []
                for qr in query_result:
                    logger.info('QUERY RESULT {0}'.format(qr))
                    amazon_key = qr.object_key + '.' + qr.object_type
                    isExist = get_object(amazon_key)
                    # append if object_key exists in amazon s3
                    if isExist['isExist'] == True:
                        data_objects.append(qr)

                return dict(status='success',data=data_objects)
            # retrieve all objects in amazon s3 and server
            else:
                query_result = db(db.media.uuid > 0).select()
                #growing
                data_objects = []
                s3_objects = get_all_objects()
        

                for qr in query_result:
                    # logger.info('QUERY RESULT {0}'.format(qr.object_key))
                    #filename.extension
                    amazon_key = qr.object_key + '.' + qr.object_type
                
                    # append if object_key exists in amazon s3
                    if amazon_key in s3_objects:
                        data_objects.append(qr)

                return dict(status='success',data=data_objects)
            
        else:
            return dict(status='fail',error='Server or communication error')


    def POST(*args, **vars):
        import tempfile
        response.view='generic.json'

        if request.args(0) == 'file':                    
            # try:       
            file = request.vars['file'] 
            if file != None:
                result = db['media'].validate_and_insert(**vars)
                logger.info('result {0}'.format(result))
                if ('id' in result):
                    object_id = result['id']['uuid']
                    query_result = db(db.media.uuid == object_id).select().first()
                
                    if query_result:
                        logger.info('Data Objects {0}'.format(query_result['object_key']))
                        key = query_result['object_key'] + "." + query_result['object_type']
                        is_uploaded = upload_file(file.file, key)
                        # is_uploaded = upload_file(os.path.join(request.folder,'static/uploads','stanford-bunny.fbx'), 'stanford-bunny.fbx')
                        logger.info('RESULT {0}'.format(is_uploaded))
                        if is_uploaded['isUploaded'] == True:
                            # amazon_result = create_presigned_url(key);
                            # logger.info('AMAZON RESULT {0}'.format(amazon_result))
                            # if amazon_result['urlCreated']:
                            #     q_result = db(db.media.id==object_id).update(amazon_uri=amazon_result['url'])
                            #     logger.info('RESULT {0}'.format(q_result))
                            return dict(status='success',message="Uploaded to bucket successfully.",data=result, query_result=query_result)
                        else: 
                            return dict(status='success',message='Server or communication error on Amazon S3',data=result)
                
                    else:
                        return dict(status="fail",data=result)
                else:
                    return dict(status="fail",data=result)
            else:
                return dict(status="fail",data=dict(errors = dict(file = T('Attach a 3D Object'))))
            # except:
            #     return dict(status="error",message=T('Server or database error.'))

        else :
            return dict(status='fail')


    def PUT(*args, **vars):

        response.view='generic.json'

        id = args[1] if len(args) else 0
        if id == 0:
            return dict(status="fail",data=dict(error='record id is required'))

        try: 
            payload = vars
            if 'file' in payload:
                payload.pop('file')

            result = db(db['media'].uuid==id).validate_and_update(**payload)
            if 'updated' in result:
                file = request.vars['file']
                if file != None:
                    query_result = db(db.media.uuid == id).select().first()

                    if query_result:
                        logger.info('Data Objects {0}'.format(query_result['object_key']))
                        key = query_result['object_key'] + "." + query_result['object_type']
                        is_uploaded = upload_file(file.file, key)
                        # is_uploaded = upload_file(os.path.join(request.folder,'static/uploads','stanford-bunny.fbx'), 'stanford-bunny.fbx')
                        logger.info('RESULT {0}'.format(is_uploaded))
                        if is_uploaded['isUploaded'] == True:
                            return dict(status='success',message="Uploaded to bucket successfully.",data=result)
                        else: 
                            return dict(status='success',message='Server or communication error on Amazon S3',data=result)
                else:
                    return dict(status="success",data=result)
            else:
                return dict(status="fail",data=result)
        except:
            return dict(status="error",message=T('Server or database error.'))


    def DELETE(*args, **vars):
        response.view='generic.json'
        if request.args(0) == 'file':

            # get record id 
            record_id = args[1] if len(args) else 0
            if record_id == 0:
                return dict(status="fail",data=dict(error='record id is required'))
            
            logger.info('RESULT {0}'.format(record_id))
            try:
                query_result = db(db.media.uuid == record_id).select().first()

                if query_result:
                    logger.info('Data Objects {0}'.format(query_result['object_key']))
                    key = query_result['object_key'] + "." + query_result['object_type']
                    result = remove_file(key)
                    logger.info('RESULT {0}'.format(result))
                    if result['isDeleted'] == True:
                        id = db(db['media'].uuid==record_id).delete()
                        return dict(status='success',data=dict(deleted=True if id>0 else False), message="Deleted to bucket successfully.")
                    else: 
                        return dict(status='success',message='Server or communication error on Amazon S3',data=dict(deleted=False))
                else:
                    return dict(status="error",message=T('Server or database error.'))

            except:
                return dict(status="error",message=T('Server or database error.'))
        else:
            return dict(status='fail', message=T('Object RECORD ID is required'))


    return locals()


