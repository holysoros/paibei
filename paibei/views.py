# -*- coding: utf-8 -*-
from pyramid.view import (
    view_defaults,
    view_config,
    forbidden_view_config,
    notfound_view_config
    )
from pyramid.response import Response
from pyramid.httpexceptions import (
    HTTPMovedPermanently,
    HTTPFound,
    HTTPNotFound,
    HTTPBadRequest,
    HTTPForbidden,
    )
from models import (
    places,
    Product,
    )
from bson.objectid import ObjectId
from gridfs import NoFile
import json


@view_config(route_name='home', renderer='templates/mytemplate.pt')
def my_view(request):
    return {'project': 'paibei'}


@view_config(route_name='add_product_page',
             request_method='GET',
             renderer='templates/add_product.pt')
def add_product_page(request):
    return {'places': places}


@view_config(route_name='product', renderer='templates/list_product.pt', request_method='GET')
def list_product(request):
    products = Product.objects.all()
    return {'products': products}

@view_config(route_name='product', request_method='POST')
def add_product(request):
    product = Product()

    product.name = request.POST['name'].strip()
    product.place = request.POST['place']
    product.elements = request.POST['elements']

    image = request.POST['image']
    product.image.put(image.file)

    product.save()

    return HTTPFound(location=request.route_url('product'))


@view_config(route_name='delete_product', request_method='POST')
def delete_product(request):
    products_to_delete = request.json_body.get('products')

    for product_id in products_to_delete:
        product = Product.objects(pk=product_id).first()
        product.delete()

    return HTTPFound(location=request.route_url('product'))


@view_config(route_name='view_image', request_method='GET')
def view_image(request):
    image_id = request.matchdict.get('image_id')
    oid = ObjectId(image_id)
    try:
        file = request.fs.get(oid)
        return Response(file.read(), content_type='image/jpeg')
    except NoFile:
        raise HTTPNotFound


@view_config(renderer='json', route_name='nfc_verify', request_method='GET')
def nfc_verify(request):
    nfc_id = request.matchdict.get('nfc_id', None)

    if nfc_id == '1':
        return {'image': 'http://www.iyi8.com/uploadfile/2014/0422/20140422124906947.jpg',
                'name': '酵素', 'prod_place': '台湾',
                'dist_place': '上海', 'serial': '512345'}
    elif nfc_id == '2':
        raise HTTPNotFound

    raise HTTPNotFound


@notfound_view_config()
def notfound(request):
    return Response(
        body=json.dumps({'message': 'Custom `Not Found` message'}),
        status='404 Not Found',
        content_type='application/json')


@forbidden_view_config()
def forbidden(request):
    return Response(
        body=json.dumps({'message': 'Custom `Unauthorized` message'}),
        status='401 Unauthorized',
        content_type='application/json')
