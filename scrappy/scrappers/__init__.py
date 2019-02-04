from .peru21 import Peru21
from .rpp import RPP
from .el_comercio import ElComercio


__all__ = ('engines',)

engines = [Peru21, RPP, ElComercio]
