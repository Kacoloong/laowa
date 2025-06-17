# -*- mode: python ; coding: utf-8 -*-
a = Analysis(
    ['51hash.py'],
    pathex=['.'],
    binaries=[('/home/ninini/.local/lib/python3.10/site-packages/z3/lib', '.')],
    datas=[],
    hiddenimports=['dis','numbers','glob','inspect','sage'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['sage'],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='51hash',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
