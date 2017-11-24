
import os
from PIL import Image
from bluelens_log import Logging
from swagger_server.models.get_objects_response import GetObjectsResponse
from swagger_server.models.get_objects_response_data import GetObjectsResponseData
from .search import Search

REDIS_SERVER = os.environ['REDIS_SERVER']
REDIS_PASSWORD = os.environ['REDIS_PASSWORD']

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

options = {
  'REDIS_SERVER': REDIS_SERVER,
  'REDIS_PASSWORD': REDIS_PASSWORD
}
log = Logging(options, tag='style-api:Products')

TMP_IMG = 'tmp.jpg'

def allowed_file(filename):
  return '.' in filename and \
         filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

class Objects(object):
  def __init__(self):
    super().__init__()

  @staticmethod
  def get_objects(file):
    search = Search(log)
    res = GetObjectsResponse()

    if file and allowed_file(file.filename):
      im = Image.open(file.stream)
      format = im.format
      log.debug(im.format)

      try:
        if 'gif' == format.lower():
          log.debug('gif')
          im.seek(0)
          mypalette = im.getpalette()
          im.putpalette(mypalette)
          new_im = Image.new("RGBA", im.size)
          new_im.paste(im)
          new_im.save('foo' + '.png')

          bg = Image.new("RGB", im.size, (255,255,255))
          bg.paste(new_im, (0,0), new_im)
          bg.save(TMP_IMG, quality=95)
          im = bg

        elif 'png' == format.lower():
          log.debug('png')
          bg = Image.new("RGB", im.size, (255,255,255))
          bg.paste(im, im)
          bg.save(TMP_IMG, quality=95)
          im = bg
        else:
          im.save(TMP_IMG)

        res_data = GetObjectsResponseData()
        boxes = search.get_objects(file.stream.getvalue())
        res_data.boxes = boxes
        res.message = "Successful"
        res.data = res_data
        response_status = 200

      except Exception as e:
        log.error(str(e))
        response_status = 400

      return res, response_status
