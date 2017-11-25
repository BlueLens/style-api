import os

from util import s3

AWS_OBJ_IMAGE_BUCKET = 'bluelens-style-object'
AWS_USER_IMAGE_BUCKET = 'bluelens-style-user-image'

AWS_ACCESS_KEY = os.environ['AWS_ACCESS_KEY'].replace('"', '')
AWS_SECRET_ACCESS_KEY = os.environ['AWS_SECRET_ACCESS_KEY'].replace('"', '')

storage = s3.S3(AWS_ACCESS_KEY, AWS_SECRET_ACCESS_KEY)

def save_image_to_storage(name, type, image_file):
  key = os.path.join(type, name + '.jpg')
  is_public = True
  file_url = storage.upload_file_to_bucket(AWS_USER_IMAGE_BUCKET, image_file, key, is_public=is_public)
  return file_url
