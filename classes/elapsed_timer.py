import time

class elapseTimer():
    """
    処理時間計測用。基準時間からcallされた時間までの差分時間を表示。
    """

    def __init__(self):

        self.init_frame()

    def init_frame(self):
        """
        保持frameのリセット
        """
        self.frame = time.time()

    def elapse_frame(self, _pre="[info] ", _suf=""):
        """
        保持フレームと現在フレームの差分表示

        Parameters
        ----------
        - pref : str
            表示テキストのプレフィックス
        - suff : str
            表示テキストのサフィックス

        Returns
        -------
        - elapsed_frame : float
            差分フレーム
        """
        get_frame = time.time()
        elapsed_frame = self.frame - get_frame
        print(f"{_pre}{elapsed_frame}{_suf}")
        self.frame = get_frame
        return elapsed_frame

