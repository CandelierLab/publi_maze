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
    '''
    Affiche récursivement l'arborescence d'un fichier HDF5 avec indentation.
    '''

    def str_node(node, prefix='', is_last=True):
      """
      Affiche récursivement un nœud HDF5 avec indentation.
      
      Args:
          node: Le nœud HDF5 à afficher
          prefix (str): Le préfixe d'indentation
          is_last (bool): Indique si c'est le dernier élément
      """

      connector = '└── ' if is_last else '├── '
      
      s = ''

      if isinstance(node, h5py.Dataset):
        s += f'{prefix}{connector}{node.name.split("/")[-1]} {node.shape} ({node.dtype})\n'
      else:
        s += f'{prefix}{connector}{node.name.split("/")[-1]}/\n'

      # Récursion pour les enfants
      if isinstance(node, h5py.Group):
        items = list(node.items())
        for i, (key, child) in enumerate(items):
          is_last_child = (i == len(items) - 1)
          extension = '    ' if is_last else '│   '
          s += str_node(child, prefix + extension, is_last_child)

      return s

    s = '─'*50 + '\n'
    s += self.filepath + '\n'

    with h5py.File(self.filepath, 'r') as f:      
      s += str_node(f, '', True)

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
  def list(tag=''):

    return os.listdir(storage.root() + tag)