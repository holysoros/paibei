from mongoengine import connect
from paibei.models import (
    Product,
    Batch,
    )

connect('paibei')
