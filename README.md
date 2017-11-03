### sync two directories

For example you have usb with some data and you want to sync it with your local hard drive.

All you have to do is provide two directories when running the script like:

```sh
#LINUX way
python sync_windows.py /destination/dir /source/dir

#WINDOWS way
you have to hardcode directories in script:
dir_base = r'<destination>'
dir_usb = r'<source>'
```

Script will check if file already exist or was modified base on data from **source**.

If doesn't exist or was modified it will copy it to exactly the same directory in **destination**.

