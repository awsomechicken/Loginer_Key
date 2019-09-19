# using Pyinstaller
import PyInstaller.__main__
import os
PyInstaller.__main__.run([
    '--clean',
    '--name=%s' % "Loginer Key Configurator",
    '--onedir', # single folder containing the executable
    #'--debug=all',
    '--windowed',
    '--hidden-import=%s' % os.path.join('.', 'TrinketCode.py'),
    '--add-binary=icon\\icon.ico;.',
    '--icon=%s' % 'icon\\icon.ico',
    'KeyConfigurator.py',
])
