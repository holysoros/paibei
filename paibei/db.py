from urlparse import urlparse
from mongoengine import connect
from mongoengine.connection import get_db
from gridfs import GridFS

def includeme(config):

    settings = config.registry.settings

    # Store DB connection in registry
    #db_url = urlparse(settings['mongo_uri'])
    #conn = pymongo.Connection(host=db_url.hostname, port=db_url.port)
    #settings['db_conn'] = conn
    connect('paibei')

    # Make DB connection accessible as a request property
    def _get_fs(request):
        #settings = request.registry.settings
        #db = settings['db_conn'][db_url.path[1:]]
        #if db_url.username and db_url.password:
            #db.authenticate(db_url.username, db_url.password)
        #return db
        db = get_db()
        return GridFS(db, collection='images')

    config.set_request_property(_get_fs, 'fs', reify=True)
