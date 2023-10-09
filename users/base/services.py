import os
import uuid

from django.core.exceptions import ValidationError
from django.db import models
from django.utils.deconstruct import deconstructible


# from nudenet import detect


# class NsfwValidator:
#     def __init__(self, allows_nsfw=False):
#         self.allows_nsfw = allows_nsfw
#
#     def __call__(self, image):
#         if not self.allows_nsfw and detect(image.read()):
#             raise ValidationError("The image contains NSFW content")


@deconstructible
class IncrementalFilename:
    def __call__(self, instance: models.Model, filename: str) -> str:
        ext = os.path.splitext(filename)[1]
        count = instance.__class__.objects.count() + 1
        filename = f"{count}_page{ext}"
        return os.path.join('brandbook/', filename)


def image_filename(instance, filename):
    """
    # Assistance from https://stackoverflow.com/questions/2673647/enforce-unique-upload-file-names-using-django
    :param instance:
    :param filename:
    :return:
    """
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return os.path.join('images/', filename)


def get_path_upload_avatar(instance, file):
    """
    Building a file path, format: (media)/avatar/user_id/photo.jpg
    :return:
    """
    return f"avatar/{instance.id}/{file}"


def validate_size_image(file_obj):
    """
    Checking file size
    :param file_obj:
    :return:
    """
    mb_limit = 2
    if file_obj.size > mb_limit * 1024 * 1024:
        raise ValidationError("The maximum file size is {size} MB".format(size=mb_limit))
