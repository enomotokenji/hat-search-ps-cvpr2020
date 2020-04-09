class BaseData:
    def __init__(self):
        self.root_dir = None
        self.gray = None
        self.div_Lint = None
        self.filenames = None
        self.L = None
        self.Lint = None
        self.mask = None
        self.M = None
        self.N = None

    def _load_mask(self):
        raise NotImplementedError

    def _load_M(self):
        raise NotImplementedError
    
    def _load_N(self):
        raise NotImplementedError

    def _to_gray(self):
        raise NotImplementedError
    
    def _div_Lint(self):
        raise NotImplementedError