from metadrive._xarray import get_drive
from metatype import Dict


class Row(Dict):

    @classmethod
    def _get(cls, url, drive):

        if '#' in url:
            url, i = url.rsplit('#', 1)
            i = int(i)
        else:
            i = 1

        drive.read_csv(url, nrows=1, skiprows=i)
        record = next(drive.df.iterrows())[1].to_dict()
        record['-'] = url
        record['@'] = drive.spec + cls.__name__
        return cls(record)

    @classmethod
    def _filter(cls, url, drive, query=None):

        drive.read_csv(url)

        for i, row in drive.df.iterrows():
            record = row.to_dict()
            record['-'] = '{}#{}'.format(url, i)
            record['@'] = drive.spec + cls.__name__
            yield cls(record)

    @classmethod
    def _update(cls, drive):
        pass
