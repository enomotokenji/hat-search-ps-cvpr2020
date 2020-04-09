import struct
import math


class Merl:
    sampling_theta_h = 90
    sampling_theta_d = 90
    sampling_phi_d = 180

    scale = [1 / 1500, 1.15 / 1500, 1.66 / 1500]

    def __init__(self, merl_file):
        """
        Initialize and load a MERL BRDF file

        :param merl_file: The path of the file to load
        """
        with open(merl_file, 'rb') as f:
            data = f.read()
            length = self.sampling_theta_h * self.sampling_theta_d * self.sampling_phi_d
            n = struct.unpack_from('3i', data)

            if n[0] * n[1] * n[2] != length:
                raise IOError("Dimmensions doe not match")

            self.brdf = struct.unpack_from(str(3 * length) + 'd', data,
                                           offset=struct.calcsize('3i'))

    def eval_raw(self, theta_h, theta_d, phi_d):
        """
        Lookup the BRDF value for given half diff coordinates

        :param theta_h: half vector elevation angle in radians
        :param theta_d: diff vector elevation angle in radians
        :param phi_d: diff vector azimuthal angle in radians
        :return: A list of 3 elements giving the BRDF value for R, G, B in
        linear RGB
        """
        return self.__eval_idx(self.__theta_h_idx(theta_h),
                               self.__theta_d_idx(theta_d),
                               self.__phi_d_idx(phi_d))

    def eval_interp(self, theta_h, theta_d, phi_d):
        """
        Lookup the BRDF value for given half diff coordinates and perform an
        interpolation over theta_h, theta_d and phi_d

        :param theta_h: half vector elevation angle in radians
        :param theta_d: diff vector elevation angle in radians
        :param phi_d: diff vector azimuthal angle in radians
        :return: A list of 3 elements giving the BRDF value for R, G, B in
        linear RGB
        """
        idx_th_p = self.__theta_h_idx(theta_h)
        idx_td_p = self.__theta_d_idx(theta_d)
        idx_pd_p = self.__phi_d_idx(phi_d)

        # Calculate the indexes for interpolation
        idx_th_p = idx_th_p if idx_th_p < self.sampling_theta_h - 1 else self.sampling_theta_h - 2
        idx_td_p = idx_td_p if idx_td_p < self.sampling_theta_d - 1 else self.sampling_theta_d - 2

        idx_th = [idx_th_p, idx_th_p + 1]
        idx_td = [idx_td_p, idx_td_p + 1]
        idx_pd = [idx_pd_p, idx_pd_p + 1]

        # Calculate the weights
        weight_th = [abs(self.__theta_h_from_idx(i) - theta_h) for i in idx_th]
        weight_td = [abs(self.__theta_d_from_idx(i) - theta_d) for i in idx_td]
        weight_pd = [abs(self.__phi_d_from_idx(i) - phi_d) for i in idx_pd]

        # Normalize the weights
        weight_th = [1 - w / sum(weight_th) for w in weight_th]
        weight_td = [1 - w / sum(weight_td) for w in weight_td]
        weight_pd = [1 - w / sum(weight_pd) for w in weight_pd]

        idx_pd[1] = idx_pd[1] if idx_pd[1] < self.sampling_phi_d else 0

        ret_val = [0] * 3

        for ith, wth in zip(idx_th, weight_th):
            for itd, wtd in zip(idx_td, weight_td):
                for ipd, wpd in zip(idx_pd, weight_pd):
                    ret_val = [r + x * wth * wtd * wpd
                               for r, x, in zip(ret_val, self.__eval_idx(ith, itd, ipd))]

        return ret_val

    def __eval_idx(self, ith, itd, ipd):
        """
        Lookup the BRDF value for a given set of indexes
        :param ith: theta_h index
        :param itd: theta_d index
        :param ipd: phi_d index
        :return: A list of 3 elements giving the BRDF value for R, G, B in
        linear RGB
        """
        ind = ipd + self.sampling_phi_d * (itd + ith * self.sampling_theta_d)

        stride = self.sampling_theta_h * self.sampling_theta_d * self.sampling_phi_d

        return [self.brdf[ind + color * stride] * s
                for s, color in zip(self.scale, range(0, 3))]

    def __theta_h_from_idx(self, theta_h_idx):
        """
        Get the theta_h value corresponding to a given index

        :param theta_h_idx: Index for theta_h
        :return: A theta_h value in radians
        """
        ret_val = theta_h_idx / self.sampling_theta_h
        return ret_val * ret_val * math.pi / 2

    def __theta_h_idx(self, theta_h):
        """
        Get the index corresponding to a given theta_h value

        :param theta_h: Value for theta_h in radians
        :return: The corresponding index for the given theta_h
        """
        if theta_h < 0:
            return 0
        th = self.sampling_theta_h * math.sqrt(theta_h / (math.pi / 2))
        return max(0, min(self.sampling_theta_h - 1,
                          math.floor(th)))

    def __theta_d_from_idx(self, theta_d_idx):
        """
        Get the theta_d value corresponding to a given index

        :param theta_d_idx: Index for theta_d
        :return: A theta_d value in radians
        """
        return theta_d_idx / self.sampling_theta_d * math.pi / 2

    def __theta_d_idx(self, theta_d):
        """
        Get the index corresponding to a given theta_d value

        :param theta_d: Value for theta_d in radians
        :return: The corresponding index for the given theta_d
        """
        return max(0, min(self.sampling_theta_d - 1,
                          math.floor(self.sampling_theta_d * theta_d / (math.pi / 2))))

    def __phi_d_from_idx(self, phi_d_idx):
        """
        Get the phi_d value corresponding to a given index

        :param phi_d_idx: Index for phi_d
        :return: A phi_d value in radians
        """
        return phi_d_idx / self.sampling_phi_d * math.pi

    def __phi_d_idx(self, phi_d):
        """
        Get the index corresponding to a given phi_d value

        :param theta_h: Value for phi_d in radians
        :return: The corresponding index for the given phi_d
        """
        while phi_d < 0:
            phi_d += math.pi

        return max(0, min(self.sampling_phi_d - 1,
                          math.floor(self.sampling_phi_d * phi_d / math.pi)))
