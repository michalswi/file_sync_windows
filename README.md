### sync two directories

For example you have usb with some data and you want to sync it with your local hard drive.

All you have to do is provide two directories when running the script like:

```sh
python sync_windows.py /destination/dir /source/dir
```

Script will check if file already exist or was modified base on data from **source**.

If doesn't exist or was modified it will copy it to exactly the same directory in **destination**.

