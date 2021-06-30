from os.path import isfile
import yaml

class YamlLoader():

    def __init__(self, _ref:str=None) -> None:

        self.path_ref = _ref
        self.params = None
        if not _ref is None:
            self.read(_ref)
        pass

    def read(self, _ref: str, _enc="utf-8"):
        """
        read file

        Parameters
        ----------
        _ref : str
            open json file path
        """
        if not isfile(_ref):
            print(f"[error] file not exist. :{_ref}")
            return None

        with open(_ref, 'r', encoding=_enc) as f:
            self.params = yaml.load(f)

    def save(self, _dst:str=None):
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

        with open(dst, mode="w", encoding="utf-8", newline="\n") as f:
            f.write(yaml.dump(self.params, default_flow_style=False))

        return True
