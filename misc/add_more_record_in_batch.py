import os
import sys
import urlparse

from mongoengine import connect
from paibei.models import (
    Product,
    Batch,
    Record,
    )
import utils


def get_batch(batch_id):
    return Batch.objects(bid=batch_id).first()


def get_current_max_index_of_batch(batch_id):
    batch = get_batch(batch_id)
    return batch.count


if __name__ == '__main__':
    connect('paibei')

    host = 'http://112.124.117.97'
    zip_dir = '/tmp/qrcode'

    import tempfile
    to_dir = tempfile.mkdtemp()
    print to_dir

    batch_id = sys.argv[1]
    added_count = sys.argv[2]

    batch = get_batch(batch_id)
    currentIndex = batch.count
    # query current record index in batch
    for i in xrange(currentIndex + 1, currentIndex + added_count + 1):
        record = Record(batch=batch, index=i,
                        serial_num=utils.generate_serial_num(),
                        left_time=batch.verify_time)
        record.save()

        url = urlparse.urljoin(host, batch.bid)
        filepath = os.path.join(to_dir, record.serial_num + '.png')
        utils.generate_qrcode(url, filepath)

    zip_filepath = os.path.join(zip_dir, batch.bid + '.zip')
    utils.zipdir(to_dir, zip_filepath)

    utils.safe_rmtree(to_dir)
