import os
import shutil


def backup_size(dic):
    size = 0
    for key in dic:
        for item in dic[key]:
            try:
                size += os.path.getsize(item)
            except:
                pass
    return size // (2 ** 20)


def volume_free_space(target):
    drive = target.split('/')[0]
    print(drive)
    total, used, free = shutil.disk_usage(drive)
    return free // (2 ** 20)
