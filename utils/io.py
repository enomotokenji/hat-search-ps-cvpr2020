import os
import json
import numpy as np


def read_txtfile(filepath):
    """Read a text file.

    Args:
        filepath (str): A path to an input text file.
    
    Returns:
        list: Text separated by \n.
    """
    with open(filepath, 'r') as f:
        txt = [l.strip() for l in f.readlines()]

    return txt


def write_txtfile(filepath, data):
    """Write a text file.

    Args:
        filepath (str): A path to an output file.
        data (list): String data. All the element of the list must be str.    
    """
    with open(filepath, 'w') as f:
        f.write('\n'.join(data))


def load_json(filepath):
    """Load a json file.

    Args:
        filepath (str): A path to an input json file.
    
    Returns:
        dict: A dictionary data loaded from a json file.
    """
    with open(filepath, 'r') as f:
        ret = json.load(f)
    
    return ret


def dump_json(filepath, data, indent=4):
    """Dump a json file.

    Args:
        filepath (str): A path to an output json file.
        data (dict): A dictionary data to be saved as a json file.
        indent (int): Indent for a json format.
    """
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=indent)


def makedirs(path):
    """Make directories.

    Args:
        path (str): A path to a directory.
    """
    if not os.path.exists(path):
        os.makedirs(path)
    
    return
