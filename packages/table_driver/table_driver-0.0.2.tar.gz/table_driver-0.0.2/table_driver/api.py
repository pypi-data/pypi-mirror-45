from metadrive._xarray import get_drive
from metatype import Dict
import json


class Row(Dict):

    @classmethod
    def _get(cls, url, drive):

        if '#' in url:
            url, i = url.rsplit('#', 1)
            i = int(i)
        else:
            i = 1

        drive.read_csv(url, nrows=1, skiprows=i)
        record = json.loads(next(drive.df.iterrows())[1].to_json())
        record['-'] = url
        record['@'] = drive.spec + cls.__name__
        return cls(record)

    @classmethod
    def _filter(cls, url, drive, query=None):

        drive.read_csv(url)

        for i, row in drive.df.iterrows():
            record = json.loads(row.to_json())
            record['-'] = '{}#{}'.format(url, i)
            record['@'] = drive.spec + cls.__name__
            yield cls(record)

    @classmethod
    def _update(cls, drive):
        pass
