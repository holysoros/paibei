import os
import random
import string
import zipfile
import datetime
import errno
import shutil
#from pinyin import PinYin
from paibei.models import (
    Product,
    Batch,
    Record,
    )

import qrcode
from PIL import Image


def id_generator(size=6, chars=string.digits+string.letters):
    return ''.join(random.choice(chars) for _ in range(size))


def safe_rmtree(path):
    try:
        shutil.rmtree(path)
    except OSError as exc:
        if exc.errno != errno.ENOENT:  # ENOENT - no such file or directory
            raise  # re-raise exception


def generate_qrcode(content, outfile):
    qr = qrcode.QRCode(
        version=5,
        error_correction=qrcode.constants.ERROR_CORRECT_Q,
        box_size=10,
        border=2,
    )

    qr.add_data(content)
    qr.make()

    im = qr.make_image()
    im = im.resize((500, 500))

    new_im = Image.new('RGB', im.size)
    new_im.paste(im, (0, 0))

    icon_width = new_im.size[0] / 3
    icon_height = new_im.size[1] / 3

    icon_pos_x = (new_im.size[0] - icon_width) / 2
    icon_pos_y = (new_im.size[1] - icon_height) / 2
    icon_size = (icon_width, icon_height)
    icon_position = (icon_pos_x, icon_pos_y)

    icon = Image.open('paibei/static/icon.png')
    icon = icon.resize(icon_size)

    new_im.paste(icon, icon_position, icon)

    new_im.save(outfile)


def zipdir(path, zip):
    try:
        import zlib
        compression = zipfile.ZIP_DEFLATED
    except:
        compression = zipfile.ZIP_STORED

    zipf = zipfile.ZipFile(zip, 'w')
    for root, dirs, files in os.walk(path):
        for file in files:
            zipf.write(os.path.join(root, file),
                       file, compress_type=compression)
    zipf.close()


def _get_pinyin_acronym(str):
    pinyin = PinYin()
    pinyin.load_word()
    words = pinyin.hanzi2pinyin(str)
    try:
        acronym = ''.join([word[0] for word in words if word])
    except IndexError:
        return None
    else:
        return acronym


def get_batch_id(batch):
    #ts = datetime.datetime.now().strftime('%y%m%d')
    #product_field = _get_pinyin_acronym(batch.product.name)
    #dist_place_field = _get_pinyin_acronym(batch.dist_place)
    #return '-'.join((ts, product_field, dist_place_field))

    return datetime.datetime.now().strftime('%y%m%d-%H-%M')


def generate_serial_num():
    while True:
        candidate_serial_num = utils.id_generator(6)
        if not Record.objects(serial_num=candidate_serial_num).first():
            return candidate_serial_num
