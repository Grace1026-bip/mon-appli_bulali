from flask import Flask

from .route import bulali
from . import models
#connection à ma bd avec sqlalchemy
models.db.init_app(bulali)

