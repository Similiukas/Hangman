# -*- mode: python -*-

block_cipher = None


a = Analysis(['Hangman.py'],
             pathex=['Z:\\Visual_Studio_2017_projects\\Hangman'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='Hangman',
          debug=False,
          strip=False,
          upx=True,
          runtime_tmpdir=None,
          console=False , icon='Z:\\Visual_Studio_2017_projects\\Hangman\\Hangman_icon.ico')
