import numpy as np
from matplotlib import pyplot as plt


def normal2color(normal, mask, dtype=np.uint8):
    """Conversion from 3D (x, y, z) surface normals to a color image representing surface normals.

    Args:
        normal (ndarray): Surface normals. The shape is H x W x 3.
        mask (ndarray): Mask with shape of H x W. The value must be 0 or 1.
        dtype (type, optional): Type of an output color image. Default to numpy.uint8.
    
    Returns:
        ndarray: A color image representing surface normals. The shape is H x W x 3.
    """
    n = normal[mask > 0]
    c = (n + 1) / 2 * np.iinfo(dtype).max
    color = np.zeros(normal.shape, dtype=dtype)
    color[mask > 0] = c

    return color


def color2normal(color, mask, dtype=None):
    """Conversion from a color image representing surface normals to 3D (x, y, z) surface normals.

    Args:
        color (ndarray): A color image representing surface normals. The shape is H x W x 3.
        mask (ndarray): Mask with shape of H x W. The value must be 0 or 1.
        dtype (type, optional): A type of an output color image. Default to None. If dtype is None, the dtype of color is used.

    Returns:
        ndarray: Surface normals. The shape is H x W x 3.
    """
    if dtype is None:
        dtype = color.dtype
    
    c = color[mask > 0]
    n = (c / np.iinfo(dtype).max * 2) - 1
    n = n / np.linalg.norm(n, axis=1, keepdims=True)

    normal = np.zeros(color.shape)
    normal[mask > 0] = n

    return normal


def calc_ange(N_est, N_gt):
    """Calculate angular errors between estimated surface normals and ground truth ones.

    Args:
        N_est (ndarray): Estimated surface normals. The shape is H x W x 3.
        N_gt (ndarray): Ground truth surface normals. The shape is H x W x 3.
    
    Returns:
        ndarray: Angular errors between N_est and N_gt. The shape is H x W.
    """
    cos = np.clip(np.sum(N_est * N_gt, axis=-1), -1, 1)
    ange = np.degrees(np.arccos(cos))

    return ange


def white_mask(img, mask, dtype=None):
    """Make background of the input image white.

    Args:
        img (ndarray): Target image. The shape is H x W x 3. The type must be numpy.uint8 or numpy.uint16.
        mask (ndarray): Mask of the img. The shape is H x W. The value must be 0 or 1.
        dtype (type): A type of the img. Default to None. If dtype is None, the dtype of img is used.
    """
    if dtype is None:
        dtype = img.dtype
    mask = np.tile(mask[..., None], (1, 1, 3))
    M = np.iinfo(dtype).max
    ret = img * mask + (-mask + 1) * M

    return ret


def save_as_color_map(filepath, data, cmap='jet', vmin=0, vmax=90):
    plt.figure()
    plt.imshow(data, cmap=cmap, vmin=vmin, vmax=vmax)
    plt.colorbar()
    plt.savefig(filepath, bbox_inches='tight')
    plt.close()