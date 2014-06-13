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
    cities,
    Product,
    Batch,
    Record,
    )
import utils
from bson.objectid import ObjectId
from gridfs import NoFile
import json
import os
import urlparse


@view_config(route_name='home', renderer='templates/mytemplate.pt')
def my_view(request):
    return {'project': 'paibei'}


@view_config(route_name='add_product_page',
             request_method='GET',
             renderer='templates/add_product.pt')
def add_product_page(request):
    return {
        'header1': 'Product',
        'header2': 'Add',
        'places': places,
        }


@view_config(route_name='product',
             renderer='templates/list_product.pt',
             request_method='GET')
def list_product(request):
    products = Product.objects.all()
    return {
        'header1': 'Product',
        'header2': 'List',
        'products': products
        }


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


@view_config(renderer='json',
             route_name='delete_product',
             request_method='DELETE')
def delete_product(request):
    prod_id = request.matchdict.get('product_id')
    product = Product.objects(pk=prod_id).first()
    product.delete()

    return {}


@view_config(route_name='delete_products', request_method='POST')
def delete_products(request):
    products_to_delete = request.json_body.get('products')

    for product_id in products_to_delete:
        product = Product.objects(pk=product_id).first()
        product.delete()

    return HTTPFound(location=request.route_url('product'))


@view_config(route_name='add_batch_page',
             request_method='GET',
             renderer='templates/add_batch.pt')
def add_batch_page(request):
    products = Product.objects.all()
    return {
        'header1': 'Batch',
        'header2': 'Add',
        'products': products,
        'cities': cities,
        }


def generate_serial_num():
    while True:
        candidate_serial_num = utils.id_generator(6)
        if not Record.objects(serial_num=candidate_serial_num).first():
            return candidate_serial_num


def generate_batch(batch):
    host = 'http://112.124.117.97'
    zip_dir = '/usr/share/nginx/html'

    import tempfile
    to_dir = tempfile.mkdtemp()
    print to_dir

    # generate all qrcode in that temp dir
    for i in xrange(1, int(batch.count)+1):
        record = Record(batch=batch, index=i,
                        serial_num=generate_serial_num(),
                        left_time=batch.verify_time)
        record.save()

        url = urlparse.urljoin(host, batch.bid)
        filepath = os.path.join(to_dir, record.serial_num + '.png')
        utils.generate_qrcode(url, filepath)

    zip_filepath = os.path.join(zip_dir, batch.bid + '.zip')
    utils.zipdir(to_dir, zip_filepath)

    utils.safe_rmtree(to_dir)


@view_config(route_name='batch', request_method='POST')
def add_batch(request):
    batch = Batch()

    batch.product = Product.objects(name=request.POST['product']).first()
    batch.dist_place = request.POST['dist_place']
    batch.count = request.POST['count']
    batch.verify_time = request.POST['verify_time']
    batch.bid = utils.get_batch_id(batch)

    batch.save()

    generate_batch(batch)

    return HTTPFound(location=request.route_url('batch'))


@view_config(route_name='batch',
             renderer='templates/list_batch.pt',
             request_method='GET')
def list_batch(request):
    batches = Batch.objects.all()
    return {
        'header1': 'Batch',
        'header2': 'List',
        'batches': batches,
        }


@view_config(route_name='delete_batches', request_method='POST')
def delete_batches(request):
    batches_to_delete = request.json_body.get('batches')

    for batch_id in batches_to_delete:
        batch = Batch.objects(pk=batch_id).first()
        batch.delete()

    return HTTPFound(location=request.route_url('batch'))


@view_config(route_name='detail_batch',
             request_method='GET',
             renderer='templates/detail_batch.pt')
def detail_batch(request):
    batch_id = request.matchdict.get('batch_id')
    batch = Batch.objects(pk=batch_id).first()

    return {
        'header1': 'Batch',
        'header2': 'Detail',
        'batch': batch
        }


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
