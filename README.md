<p align="center">
  <h3 align="center">Photometric Stereo via Discrete Hypothesis-and-Test Search</h3>
  <h4 align="center">CVPR 2020</h5>
  <p align="center"><a href="https://enomotokenji.github.io">Kenji Enomoto</a><sup>1</sup>&emsp;<a href="https://sites.google.com/view/mwaechter">Michael Waechter</a><sup>1</sup>&emsp;<a href="http://www.cs.toronto.edu/~kyros/">Kiriakos N. Kutulakos</a><sup>2</sup>&emsp;<a href="http://www-infobiz.ist.osaka-u.ac.jp/en/member/matsushita/">Yasuyuki Matsushita</a><sup>1</sup>
    <br />
    <sup>1</sup>Osaka University&emsp;<sup>2</sup>University of Toronto
    <br />
    <br />
    <a href="http://cvl.ist.osaka-u.ac.jp/wp-content/uploads/2020/04/enomoto2020photometric.pdf">Paper</a>
  </p>
</p>

---

This is the official implementation for our CVPR paper 'Photometric Stereo via Discrete Hypothesis-and-Test Search'.

# How to use

```sh
# Docker
docker build -t hat-search-ps:latest -f Dockerfile .
docker run --rm -itd --name=hat -v /path/to/any/dir:/mnt -v /path/to/hat-search-ps-cvpr2020:/hat-search-ps-cvpr2020 hat-search-ps:latest
docker exec -it hat bash
cd /hat-search-ps-cvpr2020

# Download MERL database & DiLiGenT dataset
mkdir /mnt/merl_brdf_database
sh script/download_merl_brdf_database.sh /mnt/merl_brdf_database
sh script/download_diligent_dataset.sh /mnt

# Create matrix D
python3 create_matrix_D_merl.py --N_file supp_info/N_05_interval.txt --L_file supp_info/L_diligent1.txt --merl_dir /mnt/merl_brdf_database --material_name_file supp_info/merl_name.txt --out_dir /mnt/matrix_D/diligent_1

# Compute matrix Z
python3 compute_Z_from_D.py --D_dir /mnt/matrix_D/diligent_1 --rank 3 --out_dir /mnt/matrix_Z/diligent_1/rank_3 --n_jobs -1

# Evaluate
python3 run.py --root_dir /mnt/DiLiGenT/pmsData --obj_file supp_info/diligent_name_1.txt --data_name diligent --Z_dir /mnt/matrix_Z/diligent_1/rank_3 --N_file supp_info/N_05_interval.txt --out_dir /mnt/result/diligent --n_jobs -1
```

# Citation
```
@inproceedings{enomoto2020photometric,
    title = {Photometric Stereo via Discrete Hypothesis-and-Test Search},
    author = {Kenji Enomoto and Michael Waechter and Kiriakos N. Kutulakos and Yasuyuki Matsushita},
    booktitle = {Computer Vision and Pattern Recognition (CVPR)},
    year = {2020}
}
```
