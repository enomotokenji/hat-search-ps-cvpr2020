import os
import argparse
import numpy as np
import shutil
from joblib import Parallel, delayed

import utils


def compute_z(D_dir, fname, rank, out_dir):
    D = np.load(os.path.join(D_dir, fname))

    _, u = np.linalg.eigh(D @ D.T)
    u = u[:, ::-1]
    ur = u[:, :rank]
    Z = np.eye(ur.shape[0]) - ur @ ur.T

    np.save(os.path.join(out_dir, fname), Z)


def main(D_dir, rank, out_dir, n_jobs):
    fname = utils.io.read_txtfile(os.path.join(D_dir, 'filename.txt'))
    utils.io.makedirs(out_dir)

    Parallel(n_jobs=n_jobs, verbose=5)([delayed(compute_z)(D_dir, name, rank, out_dir) for name in fname])
    shutil.copyfile(os.path.join(D_dir, 'filename.txt'), os.path.join(out_dir, 'filename.txt'))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--D_dir', type=str, help='Path to a directory storing matrices D.')
    parser.add_argument('--rank', type=int, help="M' in the original paper.")
    parser.add_argument('--out_dir', type=str, help='Path to a result directory.')
    parser.add_argument('--n_jobs', type=int, help='The maximum number of concurrently running jobs.')
    args = parser.parse_args()

    main(D_dir=args.D_dir,
         rank=args.rank,
         out_dir=args.out_dir,
         n_jobs=args.n_jobs)