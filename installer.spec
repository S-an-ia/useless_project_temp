# PyInstaller spec for ACNA_Setup.exe
# ONE single file that contains everything ? the installer GUI + the entire app

block_cipher = None

a = Analysis(
    ['installer_app.py'],
    pathex=['.'],
    binaries=[],
    datas=[
        # Bundle the entire compiled ACNA app folder as "app/" inside the installer
        ('dist\\ACNA', 'app'),
    ],
    hiddenimports=['winreg'],
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    cipher=block_cipher,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

# --onefile: everything packed into ONE exe, no extra folder needed
exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='ACNA_Setup',
    debug=False,
    strip=False,
    upx=True,
    console=False,
    icon='app.ico',
    uac_admin=True,
)
