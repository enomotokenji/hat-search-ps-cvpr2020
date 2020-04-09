import os
import argparse
import numpy as np
import cv2
from joblib import Parallel, delayed

import utils


def get_data_class(data_name):
    data_name = data_name.lower()
    if data_name == 'diligent':
        from data.diligent import DiLiGenT as Data
    else:
        raise Exception('Error.')

    return Data


def search(i, m, Z):
    return i, np.argmin(np.linalg.norm(np.dot(Z, m), axis=1))


def main(root_dir, obj_file, data_name, Z_dir, N_file, out_dir, n_jobs):
    obj_name = utils.io.read_txtfile(obj_file)
    fname = utils.io.read_txtfile(os.path.join(Z_dir, 'filename.txt'))
    Z = np.array([np.load(os.path.join(Z_dir, name)) for name in fname])
    N = np.loadtxt(N_file)

    Data = get_data_class(data_name)

    for i_obj, obj_name in enumerate(obj_name):
        utils.io.makedirs(os.path.join(out_dir, obj_name))
        data = Data(os.path.join(root_dir, obj_name))

        mask = data.mask
        M = data.M[:, mask > 0]

        ret = Parallel(n_jobs=n_jobs, verbose=5)([delayed(search)(i, m, Z) for i, m in enumerate(M.T)])
        ret.sort(key=lambda x: x[0])
        idx = np.array([x[1] for x in ret])

        N_est = np.zeros(data.mask.shape + (3,))
        N_est[data.mask > 0] = N[idx]

        np.save(os.path.join(out_dir, obj_name, 'N_est.npy'), N_est * np.tile(data.mask[..., None], (1, 1, 3)))
        N_est_color = utils.ps.normal2color(N_est, data.mask)
        N_est_color = N_est_color[:, :, ::-1]
        cv2.imwrite(os.path.join(out_dir, obj_name, 'N_est.png'), utils.ps.white_mask(N_est_color, data.mask, dtype=np.uint8))

        if data.N is not None:
            N_gt = data.N
        else:
            print('=====\n{} - {} done\n====='.format(i_obj, obj_name))
            continue
        
        # evaluate
        result = {}
        ange_map = utils.ps.calc_ange(N_gt=N_gt, N_est=N_est) * data.mask
        np.save(os.path.join(out_dir, obj_name, 'ange_map.npy'), ange_map)
        result['MAngE'] = np.mean(ange_map[data.mask > 0])
        N_gt_color = utils.ps.normal2color(N_gt, data.mask)
        N_gt_color = N_gt_color[:, :, ::-1]
        cv2.imwrite(os.path.join(out_dir, obj_name, 'N_gt.png'), utils.ps.white_mask(N_gt_color, data.mask, dtype=np.uint8))
        utils.ps.save_as_color_map(filepath=os.path.join(out_dir, obj_name, 'ange_map.pdf'), data=ange_map, vmax=20)
        utils.io.dump_json(filepath=os.path.join(out_dir, obj_name, 'result.json'), data=result)

        for key, value in result.items():
            print('{}: {}'.format(key, value))

        print('=====\n{} - {} done\n====='.format(i_obj, obj_name))

    return


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--root_dir', type=str, help='Path to a directory storing dataset.')
    parser.add_argument('--obj_file', type=str, help='Path to a text file for object names.')
    parser.add_argument('--data_name', type=str, help='One of the pre-defined dataset names. "diligent"')
    parser.add_argument('--Z_dir', type=str, help='Path to a directory storing matrices Z.')
    parser.add_argument('--N_file', type=str, help='Path to a text file of surface normal candidates.')
    parser.add_argument('--out_dir', type=str, help='Path to a result directory.')
    parser.add_argument('--n_jobs', type=int, help='The maximum number of concurrently running jobs.')
    args = parser.parse_args()

    main(root_dir=args.root_dir,
         obj_file=args.obj_file,
         data_name=args.data_name,
         Z_dir=args.Z_dir,
         N_file=args.N_file,
         out_dir=args.out_dir,
         n_jobs=args.n_jobs)
