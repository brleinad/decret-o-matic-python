# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

import os

dir_path = os.getcwd()
data_path = os.path.join('decretomatic', 'data')

a = Analysis(['decret-o-matic.py'],
             pathex=[dir_path],
             binaries=[],
             datas=[(data_path, data_path),],
             hiddenimports=['packaging.requirements', 'pkg_resources.py2_warn'],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='decret-o-matic',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=True )
