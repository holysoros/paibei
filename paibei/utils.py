import os
import random
import urlparse
import string

import qrcode
from PIL import Image


def id_generator(size=6, chars=string.digits+string.letters):
    return ''.join(random.choice(chars) for _ in range(size))


def generate_qrcode_for_record(serial_num):
    host = 'http://paibei.com'
    to_dir = '/tmp/qrcode'

    url = urlparse.urljoin(host, serial_num)
    outfile = os.path.join(to_dir, serial_num + '.png')
    generate_qrcode(url, outfile)


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
