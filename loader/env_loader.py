from os.path import isfile

class EnvLoader():

    def __init__(self, _ref) -> None:
        self.path_ref = _ref
        self.params = {}
        if not _ref is None:
            self.params = self.read(_ref)
        pass

    def read(self, _path):
        """
        read envfile
        """
        if not isfile(_path):
            print(f"[info] not exist env file. {_path}")
            return None

        # ファイル行読みしながらテキスト置き換え
        with open(_path, 'r', encoding="utf8") as f:
            ret = {}
            while True:
                line = f.readline()
                if line:
                    spl = line.replace('\n', '').split("=", 2)
                    ret[spl[0]] = spl[1]
                else:
                    break
            return ret

    def input_params(self, _keys:list):
        """
        update env param
        """
        ret = {}
        for key in enumerate(_keys):
            _input = input(f"input {key} value. :")
            self.params[key] = _input
        return ret

    def get(self, _key):
        """
        update env param
        """
        if _key in self.params:
            return self.params[_key]
        return None

    def set(self, _key:str, _val):
        """
        update env param
        """
        self.params[_key] = _val

    def save(self, _dst=None, _params=None):
        """
        dictを.envに変換

        Parameters
        ----------
        - _dst : str
            保存先変更時パス
        - _params : str
            外部dict
        """
        dst = self.path_ref
        if not _dst is None:
            dst = _dst
        new_lines = ""
        ref_params = self.params
        if not _params is None:
            ref_params = _params
        for k, v in ref_params.items():
            new_lines += f"{k}={v}\n"
        # ファイル名保存
        with open(dst, mode="w", encoding="utf8", newline="\n") as f:
            f.write(new_lines)
        return True

