#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
from datetime import datetime
from pathlib import Path
import piexif
import subprocess


def fixexif(dp):
    '''
    Fix EXIF for images in a folder

    :param dp: Path to folder to fix
    '''
    for fp in dp.iterdir():
        # focus only on files from WhatsApp
        if "-WA" not in str(fp.name):
            continue
        # focus on images without Exif
        exif_dict = piexif.load(str(fp))
        if not exif_dict['Exif']:
            # image without Exif
            # get date from IMG-YYYYMMDD-WAXXXX.jpg
            date_str = str(fp.name).split("-")[1]
            date = datetime.strptime(date_str, '%Y%m%d').strftime("%Y:%m:%d %H:%M:%S")
            # add date to Exif
            exif_dict['Exif'][piexif.ExifIFD.DateTimeOriginal] = date
            piexif.insert(piexif.dump(exif_dict), str(fp))

        print(fp.name)
        if len(exif_dict['Exif']) == 1:
            # image with issue in jpg
            # use sips (only on Mac)
            cmd = "sips --setProperty format jpeg --setProperty formatOptions 100 \
                %s --out %s" % (fp, fp)
            subprocess.run(cmd, shell=True, check=True)
        else:
            print(exif_dict['Exif'])

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Fix EXIF for WhatsApp images')
    parser.add_argument('--dp', required=True, help="Path to folder with images to fix")
    args = parser.parse_args()

    fixexif(Path(args.dp))