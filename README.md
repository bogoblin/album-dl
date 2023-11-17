# Album Downloader

An easy-to-use web interface for downloading albums from
YouTube Music.

A single exe is compiled in `dist/album-dl.exe` if you just want to
run the program. Otherwise you can run the app with python 3.

Feel free to make issues if you find any bugs or anything.

Currently building for Windows with:

```shell
pyinstaller.exe py_src\app.py -F --add-data "py_src\templates:templates"  --collect-data ytmusicapi
```