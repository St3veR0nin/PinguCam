cd %0/../

py -3.6 -m pip install --upgrade PyInstaller

py -3.6 -m PyInstaller -y -w -F -i images/icon.ico --hidden-import pygame --hidden-import pynput --hidden-import pyaudio --hidden-import screeninfo PinguCam_alpha.py

move dist\PinguCam_alpha.exe PinguCam_alpha.exe

rmdir /s /q dist

rmdir /s /q build

rm PinguCam_alpha.spec