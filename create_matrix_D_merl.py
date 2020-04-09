import os
import argparse
import numpy as np
from tqdm import tqdm

import utils
from merl import Merl


def color2gray(x):
    return 0.3 * x[0] + 0.59 * x[1] + 0.11 * x[2]


def main(N_file, L_file, merl_dir, material_name_file, out_dir):
    N = np.loadtxt(N_file)
    L = np.loadtxt(L_file)
    mat_name = utils.io.read_txtfile(material_name_file)

    v = np.array([0, 0, 1], dtype=np.float)
    H = (L + v) / np.linalg.norm(L + v, axis=1, keepdims=True)
    theta_d = np.arccos(np.sum(L * H, axis=1))
    norm = np.linalg.norm(L - H, axis=1, keepdims=True)
    norm[norm == 0] = 1
    Q = (L - H) / norm

    print('Creating matrix D...')
    D = np.zeros((len(N), len(L), len(mat_name)), dtype=np.float)
    for k, name in enumerate(tqdm(mat_name)):
        merl = Merl(os.path.join(merl_dir, name+'.binary'))
        for i, n in enumerate(N):
            nl = L @ n
            theta_h = np.arccos(H @ n)
            norm = np.linalg.norm(H - n, axis=1, keepdims=True)
            norm[norm == 0] = 1
            P = (H - n) / norm
            phi_d = np.arccos(np.clip(np.sum(P * Q, axis=1), -1., 1.))
            for j in range(len(L)):
                if nl[j] <= 0:
                    continue
                rho = np.array(merl.eval_interp(theta_h=theta_h[j], theta_d=theta_d[j], phi_d=phi_d[j]))
                rho[rho < 0] = 0
                D[i, j, k] = color2gray(rho * nl[j])

    D = D / np.max(D, axis=1)[:, None]

    print('Saving matrix D...')
    utils.io.makedirs(out_dir)
    fname = []
    for i, D_ in enumerate(tqdm(D)):
        name = '{:06d}.npy'.format(i)
        fname.append(name)
        np.save(os.path.join(out_dir, name), D_)
    utils.io.write_txtfile(os.path.join(out_dir, 'filename.txt'), fname)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--N_file', type=str, help='Path to a text file of surface normal candidates.')
    parser.add_argument('--L_file', type=str, help='Path to a text file of light directions.')
    parser.add_argument('--merl_dir', type=str, help='Path to a directory storing the MERL binary files.')
    parser.add_argument('--material_name_file', type=str, help='Path to a text file of material names.')
    parser.add_argument('--out_dir', type=str, help='Path to a result directory.')
    args = parser.parse_args()

    main(N_file=args.N_file,
         L_file=args.L_file,
         merl_dir=args.merl_dir,
         material_name_file=args.material_name_file,
         out_dir=args.out_dir)
