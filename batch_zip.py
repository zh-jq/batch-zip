#!/bin/env python3

from zipfile import ZipFile, ZIP_DEFLATED
import os
import sys
import shutil


def zip_write_nested_file(z_file, f_path, prefix):
    name = os.path.basename(f_path)
    a_name = "{}/{}".format(prefix, name)
    if os.path.isfile(f_path):
        z_file.write(f_path, a_name)
    if os.path.isdir(f_path):
        for d in os.listdir(f_path):
            zip_write_nested_file(z_file, os.path.join(f_path, d), a_name)


def zip_write_file(z_file, f_path):
    name = os.path.basename(f_path)
    if os.path.isfile(f_path):
        z_file.write(f_path, name)
    if os.path.isdir(f_path):
        for d in os.listdir(f_path):
            zip_write_nested_file(z_file, os.path.join(f_path, d), name)


def zip_dir(target_dir, d_path):
    d_name = os.path.basename(d_path)
    z_path = "{}/{}.zip".format(target_dir, d_name)
    with ZipFile(z_path, mode='x', compression=ZIP_DEFLATED) as z_file:
        for d in os.listdir(d_path):
            zip_write_file(z_file, os.path.join(d_path, d))
    return z_path


STEP = 10
count = 10
batch = 0

too_large_dir = "too_large"
if not os.path.isdir(too_large_dir):
    os.mkdir(too_large_dir)

target_dir = sys.argv[1]
dirs = os.listdir(target_dir)
for d in dirs:
    d_path = os.path.join(target_dir, d)
    if os.path.isdir(d_path):
        if count >= STEP:
            count = 1
            batch += 1
        else:
            count += 1
        sub_dir = "batch{}".format(batch)
        if not os.path.isdir(sub_dir):
            os.mkdir(sub_dir)

        print("try to zip {}".format(d))
        z_path = zip_dir(sub_dir, d_path)
        print("{} zipped into {}".format(d, sub_dir))

        if os.path.getsize(z_path) > 50_000_000:
            shutil.move(z_path, too_large_dir)
            print("{} is too large, moved to {}".format(d, too_large_dir))
