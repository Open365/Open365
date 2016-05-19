import os
import shutil


def copy_with_ownership(src, dst):
    shutil.copytree(src, dst,  copy_function=_copy2_with_ownership)


def _copy2_with_ownership(filea, fileb):
    shutil.copy2(filea, fileb)
    stat_a = os.stat(filea)
    os.chown(fileb, stat_a.st_uid, stat_a.st_gid)
