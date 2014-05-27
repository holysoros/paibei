from pyramid.view import view_config
from pyramid.response import Response
from models import (
    places,
    Product,
)
from pyramid.httpexceptions import (
    HTTPMovedPermanently,
    HTTPFound,
    HTTPNotFound,
    HTTPBadRequest,
    HTTPForbidden,
    )
from bson.objectid import ObjectId
from gridfs import NoFile


@view_config(route_name='home', renderer='templates/mytemplate.pt')
def my_view(request):
    return {'project': 'paibei'}


@view_config(route_name='add_product_page',
             request_method='GET',
             renderer='templates/add_product.pt')
def add_product_page(request):
    return {'places': places}


@view_config(route_name='add_product', request_method='POST')
def add_product(request):
    product = Product()

    product.name = request.POST['name'].strip()
    product.place = request.POST['place']
    product.elements = request.POST['elements']

    #import pdb; pdb.set_trace()
    image = request.POST['image']
    product.image.put(image.file)

    product.save()
    import pdb; pdb.set_trace()

    return Response("Successfully")
    #return HTTPFound(location=request.route_url(''))


@view_config(route_name='view_image', request_method='GET')
def view_image(request):
    image_id = request.matchdict.get('image_id')
    oid = ObjectId(image_id)
    try:
        file = request.fs.get(oid)
        return Response(file.read(), content_type='image/jpeg')
    except NoFile:
        raise HTTPNotFound
