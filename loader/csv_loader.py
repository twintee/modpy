from os.path import isfile
import csv

class CsvLoader():

    def __init__(self, _ref:str=None, _enc='utf-8', _skip_header=False) -> None:
        """
        read file

        Parameters
        ----------
        _ref : str
            csv file path
        _enc : str
            encoder 'utf-8' or 'shift_jis' or 'euc_jp'
        _skip_header : str
            csv file path
        """

        self.path_ref = _ref
        self.params = []
        if not _ref is None:
            self.read(_ref, _skip_header)
        pass

    def read(self, _ref:str, _enc='utf-8', _skip_header=False):
        """
        read file

        Parameters
        ----------
        _ref : str
            csv file path
        _enc : str
            csv file path
        _enc : str
            csv file path
        """
        if not isfile(_ref):
            print(f"[info] file not exist. :{_ref}")
            return False

        self.params = []
        with open(_ref, 'r', encoding=_enc) as f:
            csv_reader = csv.reader(f, delimiter=',', quotechar='"')
            if _skip_header:
                next(csv_reader)
                _skip_header = False
            for row in csv_reader:
                print(','.join(row))
                self.params.append(row)
        return True

    def addrow(self, _row):
        """
        set row

        Parameters
        ----------
        _row : list
        """
        if len(self.params) > 0:
            if len(self.params[0]) != len(_row):
                print(f"[error] added row columns count error. : original[{len(self.params[0])}] - added[{len(_row)}]")
                return False
        self.params.append(_row)
        return True

    def save(self, _dst:str=None, _enc='utf-8', _skip_header=False):
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

        for r in self.params:
            if _skip_header:
                _skip_header = False
                continue
            with open(dst, 'a', newline="\n", encoding=_enc) as f:
                writer = csv.writer(f)
                writer.writerow(r)
        return True
