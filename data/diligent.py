import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import numpy as np
import cv2
from tqdm import tqdm
from scipy import io

import utils
from .base import BaseData


class DiLiGenT(BaseData):
    def __init__(self, root_dir, gray=True, div_Lint=True):
        super().__init__()
        self.root_dir = root_dir
        self.gray = gray
        self.div_Lint = div_Lint
        self.filenames = utils.io.read_txtfile(os.path.join(root_dir, 'filenames.txt'))
        self.L = np.loadtxt(os.path.join(root_dir, 'light_directions.txt'))
        self.Lint = np.loadtxt(os.path.join(root_dir, 'light_intensities.txt'))
        self.mask = cv2.imread(os.path.join(root_dir, 'mask.png'), 0) / 255.
        self.N = io.loadmat(os.path.join(self.root_dir, 'Normal_gt.mat'))['Normal_gt']
        self.M = self._load_M()

        self._div_Lint()
        self._to_gray()


    def _load_M(self):
        M = []
        for fname in tqdm(self.filenames):
            img = cv2.imread(os.path.join(self.root_dir, fname), -1)
            img = img[..., :3]
            img = img[..., ::-1]
            M.append(img)
        M = np.array(M, dtype=np.float) / np.iinfo(np.uint16).max

        return M
    
    def _div_Lint(self):
        self.M /= self.Lint[:, None, None]

    def _to_gray(self):
        if self.gray:
            self.M = np.mean(self.M, axis=-1)
