from os.path import isfile
import json

class JsonLoader():

    def __init__(self, _ref:str=None) -> None:

        self.path_ref = _ref
        self.params = None
        if not _ref is None:
            self.read(_ref)
        pass

    def read(self, _ref: str, _enc="utf-8"):
        """
        read json file

        Parameters
        ----------
        _ref : str
            open json file path
        """
        if not isfile(_ref):
            print(f"[error] json file not exist. :{_ref}")
            return None

        with open(_ref, 'r', encoding=_enc) as f:
            self.params = json.load(f)

    def get(self, _ref: str):
        """
        read json file
        """
        return self.params

    def save(self, _dst:str=None):
        """
        save json file

        Parameters
        ----------
        _dst : str
            save json file path
        """
        dst = str(self.path_ref)
        if not _dst is None:
            dst = _dst

        with open(dst, mode="w", encoding="utf-8", newline="\n") as f:
            json.dump(self.params, f, indent=4, ensure_ascii=False)

        return True
