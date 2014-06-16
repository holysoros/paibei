from pyramid.config import Configurator
from pyramid.session import UnencryptedCookieSessionFactoryConfig
from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings)

    session_factory = UnencryptedCookieSessionFactoryConfig('itsaseekreet')
    authn_policy = AuthTktAuthenticationPolicy('paibei', hashalg='sha512')
    authz_policy = ACLAuthorizationPolicy()
    config.set_session_factory(session_factory)
    config.set_authentication_policy(authn_policy)
    config.set_authorization_policy(authz_policy)

    config.include('pyramid_chameleon')
    config.include('.db')

    config.add_static_view('static', 'static', cache_max_age=3600)

    config.include(add_admin_route)
    config.include(add_api_route)
    config.include(add_mobile_web_route)

    config.scan()
    return config.make_wsgi_app()


def add_admin_route(config):
    config.add_route('view_image', '/images/{image_id}')
    config.add_route('admin_index', '/admin')
    config.add_route('product', '/admin/products')
    config.add_route('delete_product', '/products/{product_id}/delete')
    config.add_route('delete_products', '/admin/products/delete')
    config.add_route('add_product_page', '/admin/products/new')
    config.add_route('edit_product_page', '/admin/products/{product_id}/edit')
    config.add_route('modify_product', '/admin/products/{product_id}')

    config.add_route('add_batch_page', '/admin/batches/add')
    config.add_route('batch', '/admin/batches')
    config.add_route('delete_batches', '/admin/batches/delete')
    config.add_route('detail_batch', '/admin/batches/{batch_id}')
    config.add_route('import_nfc', '/admin/batches/{batch_id}/importnfc')


def add_api_route(config):
    config.add_route('nfc_verify', '/nfc/{nfc_id}')


def add_mobile_web_route(config):
    config.add_route('qrcode_verify', '/{qrcode_id:[a-zA-Z0-9]{6}}')
    config.add_route('qrcode_verify_result', '/{qrcode_id:[a-zA-Z0-9]{6}}/r')
    config.add_route('contact_us', '/w/contact_us')
