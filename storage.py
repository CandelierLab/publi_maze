'''
Storage
'''

import os
from collections import UserDict
import re
import h5py
import numpy as np

class storage(UserDict):

  # ────────────────────────────────────────────────────────────────────────
  def __init__(self, tag, ext='h5'):

    # Check path
    if tag[0]!='/':
      tag = storage.root() + tag

    # Check extension
    match ext:
      case 'h5':
        if re.search('\\.h5$', tag) is None:
          tag += '.h5'

    # File path
    self.filepath = tag

    # ─── Checks

    # Create folder if not existing
    dir = os.path.dirname(self.filepath)
    if not os.path.exists(dir):      
      os.makedirs(dir, exist_ok=True)

  # ────────────────────────────────────────────────────────────────────────
  def __str__(self):
     
    def visitor_func(name, node):

      global s
      s = ''

      if isinstance(node, h5py.Dataset):
        s += node.name + f' {node.shape}'
      else:
        s += node.name

    with h5py.File(self.filepath, 'r') as f:

      f.visititems(visitor_func)

      # print(f.keys())

    return s

  # ────────────────────────────────────────────────────────────────────────
  def exists(self):

    return os.path.exists(self.filepath)
  
  # ────────────────────────────────────────────────────────────────────────
  def contains(self, key):
    '''
    Check if the key is in the file 

    Args:
        key (_type_): _description_

    Returns:
        bool
    '''

    with h5py.File(self.filepath, 'r') as f:
      return key in f
    return None

  # ────────────────────────────────────────────────────────────────────────
  def __setitem__(self, key, value):
    '''
    Saving data.

    Args:
        key (_type_): _description_
        value (_type_): _description_

    Returns:
        _type_: _description_
    '''

    with h5py.File(self.filepath, 'a') as f:

      # Remove previous dataset
      if key in f: del f[key]

      # New dataset
      f.create_dataset(key, data=value)
  
  # ────────────────────────────────────────────────────────────────────────
  def __getitem__(self, key):
    '''
    Loading data.

    Args:
        key (_type_): _description_
    '''

    with h5py.File(self.filepath, 'r') as f:
      return np.array(f[key]) if f[key].size==1 else np.array(f[key][:])

    return None

  # ────────────────────────────────────────────────────────────────────────
  @staticmethod
  def root():
    return os.getcwd() + os.sep + 'Files' + os.sep

  # ────────────────────────────────────────────────────────────────────────
  @staticmethod
  def list(tag):

    return os.listdir(storage.root() + tag)