# -*- mode: python ; coding: utf-8 -*-
# PyInstaller spec for "Useless Alarm Clock"
# Run: pyinstaller alarm.spec

block_cipher = None

# Data files to bundle alongside the .exe
datas = [
    ('images', 'images'),
    ('Alarm Beeps.wav',  '.'),
    ('Alarm Clock.wav',  '.'),
    ('Loud alarm.wav',   '.'),
    ('Trumpets.wav',     '.'),
]

a = Analysis(
    ['frontend.py'],
    pathex=['.'],
    binaries=[],
    datas=datas,
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='ACNA',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='app.ico',
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='ACNA',
)
