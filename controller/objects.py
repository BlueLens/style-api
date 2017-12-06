
import os
from PIL import Image
import uuid
from bluelens_log import Logging
from swagger_server.models.get_objects_response import GetObjectsResponse
from swagger_server.models.get_objects_response_data import GetObjectsResponseData
import stylelens_product
from swagger_server.models.product import Product
from .search import Search
from util import utils

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
  def get_objects_by_image_file(file):
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

        product_api = stylelens_product.ImageApi()
        image = stylelens_product.Image() # Product | Product object that needs to be added to the db.
        image_url = utils.save_image_to_storage(str(uuid.uuid4()), 'camera', TMP_IMG)
        with open(TMP_IMG, 'rb') as im_f:
          img_data = im_f.read()
        boxes = search.get_objects(img_data)


        for box_obj in boxes:
          products = []
          for prod in box_obj.products:
            products.append(Product.from_dict(prod))
          box_obj.products = products

        image.boxes = boxes
        image.url = image_url
        api_res = product_api.add_image(image)
        image_id = api_res.data.image_id

        res_data = GetObjectsResponseData()
        res_data.boxes = boxes
        res_data.image_id = image_id
        res.message = "Successful"
        res.data = res_data
        response_status = 200

      except Exception as e:
        log.error(str(e))
        response_status = 400

      return res, response_status

  @staticmethod
  def get_objects_by_product_id(product_id):
    search = Search(log)
    res = GetObjectsResponse()

    try:
      res_data = GetObjectsResponseData()
      boxes = search.get_objects_by_product_id(product_id)
      res_data.boxes = boxes
      res.message = "Successful"
      res.data = res_data
      response_status = 200

    except Exception as e:
      log.error(str(e))
      response_status = 400

    return res, response_status
