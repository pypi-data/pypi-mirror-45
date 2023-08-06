__site_url__ = '*://*xlsx|*csv#sheet-rowid'

from metadrive._xarray import get_drive

def _login():
    return get_drive()
