from fractions import Fraction
from io import FileIO
import exifread
from exifread.exif_log import setup_logger
import os
# import pyexiv2
from iptcinfo3 import IPTCInfo


def read_exif_tag(exiftags, tagname):
    return exiftags[tagname] if tagname in exiftags else None

def strip_common_prefix(phrase: str, prefix_phrase: str):
    prefix = []
    for i, o in zip(phrase.split(' '), prefix_phrase.split(' ')):
        if i == o:
            prefix.append(i)
        else:
            break
    return phrase.removeprefix(' '.join(prefix)).strip()

# print(strip_common_prefix('NIKON D3100', 'NIKON CORPORATION' + ' '))
# exit()
cameras_seen = set()
directory = "G:\Pictures\TV"
# setup_logger(True, True)
for filename in os.listdir(directory):
    f = os.path.join(directory, filename)
    # checking if it is a file
    if os.path.isfile(f):
        img = f
        exiffile = open(img, "rb")
        try:
            exiftags = exifread.process_file(exiffile, details=False)
            camera_make = read_exif_tag(exiftags, 'Image Make')
            camera_model = read_exif_tag(exiftags, 'Image Model')
            if camera_make and camera_model :
                camera = f"{str(camera_make).strip()} {strip_common_prefix(str(camera_model), str(camera_make) + ' ')}"
            elif camera_make:
                camera = str(camera_make)
            elif camera_model:
                camera = str(camera_model)
            else:
                camera = None
            lens = read_exif_tag(exiftags, 'EXIF LensModel')
            if camera and lens:
                camera_description = f"Camera / Lens: {camera} / {str(lens)}"
            elif camera:
                camera_description = f"Camera: {camera}"
            elif lens:
                camera_description = f"Lens: {str(lens)}"
            else:
                camera_description = ''
            details = []
            focal_length = read_exif_tag(exiftags, 'EXIF FocalLength')
            if focal_length:
                details.append(f"{str(focal_length.values[0].decimal())} mm")
            exposure_time = read_exif_tag(exiftags, 'EXIF ExposureTime')
            if exposure_time:
                try:
                    exposure_time = exposure_time.values[0]
                    if exposure_time.numerator > 1:
                        exposure_time = Fraction(1, round(exposure_time.denominator / exposure_time.numerator))
                except Exception as e:
                    print(f'Error modifying shutter speed {str(exposure_time)}')
                    print(e)
                details.append(f"{str(exposure_time)} sec.")
            f_stop = read_exif_tag(exiftags, 'EXIF FNumber')
            if f_stop:
                details.append(f"f/{str(f_stop.values[0].decimal())}")
            iso_speed = read_exif_tag(exiftags, 'EXIF ISOSpeedRatings')
            if iso_speed:
                details.append(f"ISO {str(iso_speed)}")
            if 'EXIF DateTimeOriginal' in exiftags:
                datetime = exiftags['EXIF DateTimeOriginal'].values
                # sometimes exif date returns useless data, probably no date set on camera
                if datetime == '0000:00:00 00:00:00':
                    datetime = ''
                else:
                    try:
                        # localize the date format
                        date = datetime[:10].split(':')
                        time = datetime[10:]
                        # if DATEFORMAT[1] == 'm':
                        #     datetime = date[1] + '-' + date[2] + '-' + date[0] + '  ' + time
                        # elif DATEFORMAT[1] == 'd':
                        #     datetime = date[2] + '-' + date[1] + '-' + date[0] + '  ' + time
                        # else:
                        datetime = date[0] + '-' + date[1] + '-' + date[2] + ' ' + time
                    except:
                        pass
                    exif = True
            print (img)
            if camera_description:
                print(" - " + camera_description)
            if len(details) > 0:
                print(" - " + ' '.join(details))
            print (" - " + datetime)
        except Exception as e:
            pass
        exiffile.close()
# # get iptc title, description and keywords
# iptcfile = open(img[0], "rb")
# try:
#     iptc = IPTCInfo(iptcfile)
#     print(iptc)
#     if iptc['headline']:
#         title = bytes(iptc['headline']).decode('utf-8')
#         iptc_ti = True
#     if iptc['caption/abstract']:
#         description = bytes(iptc['caption/abstract']).decode('utf-8')
#         iptc_de = True
#     if iptc['keywords']:
#         tags = []
#         for tag in iptc['keywords']:
#             tags.append(bytes(tag).decode('utf-8'))
#         keywords = ', '.join(tags)
#         iptc_ke = True
# except Exception as e:
#     print(e)
# iptcfile.close()

# metadata = pyexiv2.ImageMetadata(img[0])
# metadata.read()
# print (metadata)