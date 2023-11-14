# Album Downloader

An easy-to-use web interface for downloading albums from
YouTube Music.

It's not really done yet - when you download an album it 
just says 'Downloading...' and doesn't update the UI. I
will sort this out soon. However, it is downloading, and
it does finish if you wait for it.

Feel free to make issues if you find any bugs or anything.

Currently building for Windows with:

```shell
pyinstaller.exe py_src\app.py -F --add-data "py_src\static:static" --add-data "py_src\templates:templates"  --collect-data ytmusicapi
```

Version 0.2