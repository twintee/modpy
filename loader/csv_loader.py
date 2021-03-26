from os.path import isfile
import csv

class CsvLoader():

    def __init__(self, _ref:str=None) -> None:

        self.path_ref = _ref
        self.params = []
        if not _ref is None:
            self.read(_ref)
        pass

    def read(self, _ref:str, _enc='utf-8', _noheader=False):
        """
        read file

        Parameters
        ----------
        _ref : str
            open file path
        """
        if not isfile(_ref):
            print(f"[error] json file not exist. :{_ref}")
            return None

        self.params = []
        with open(_ref, 'r', encoding=_enc) as f:
            csv_reader = csv.reader(f, delimiter=',', quotechar='"')
            if _noheader:
                next(csv_reader)
            for row in csv_reader:
                print(','.join(row))
                self.params.append(row)

    def get(self):
        """
        get params
        """
        return self.params

    def set(self, _row):
        """
        set row

        Parameters
        ----------
        _row : list
        """
        self.params.append(_row)
        return True

    def save(self, _dst:str=None, _enc='utf-8'):
        """
        save file

        Parameters
        ----------
        _dst : str
            save file path
        """
        dst = str(self.path_ref)
        if not _dst is None:
            dst = _dst

        with open(dst, 'w', newline="\n", encoding=_enc) as f:
            writer = csv.writer(f)
            writer.writerows(self.params)
        return True
