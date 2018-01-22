
import os
import PIL
import uuid
import redis
import pickle
from bluelens_log import Logging
from swagger_server.models.get_objects_response import GetObjectsResponse
from swagger_server.models.get_objects_response_data import GetObjectsResponseData
from swagger_server.models.get_objects_by_image_id_response import GetObjectsByImageIdResponse
from swagger_server.models.box_object import BoxObject
from swagger_server.models.image import Image
from stylelens_user.users import Users
from .search import Search
from util import utils

REDIS_SERVER = os.environ['REDIS_SEARCH_SERVER']
REDIS_PASSWORD = os.environ['REDIS_SEARCH_PASSWORD']

REDIS_INDEXED_IMAGE_HASH = 'bl_indexed_image_hash'
REDIS_INDEXED_IMAGE_LIST = 'bl:indexed:image:list'
REDIS_INDEXED_OBJECT_HASH = 'bl_indexed_object_hash'
REDIS_INDEXED_OBJECT_LIST = 'bl:indexed:object:list'

REDIS_USER_OBJECT_HASH = 'bl:user:object:hash'
REDIS_USER_OBJECT_QUEUE = 'bl:user:object:queue'
REDIS_USER_IMAGE_HASH = 'bl:user:image:hash'
REDIS_FEED_IMAGE_HASH = 'bl:feed:image:hash'

REDIS_LOG_SEARCH_IMAGE_FILE_QUEUE = 'bl:log:search:image:file'
REDIS_LOG_SEARCH_IMAGE_ID_QUEUE = 'bl:log:search:image:id'
REDIS_LOG_SEARCH_OBJECT_ID_QUEUE = 'bl:log:search:object:id'

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

options = {
  'REDIS_SERVER': REDIS_SERVER,
  'REDIS_PASSWORD': REDIS_PASSWORD
}
log = Logging(options, tag='style-api:Objects')

rconn = redis.StrictRedis(REDIS_SERVER, decode_responses=False, port=6379, password=REDIS_PASSWORD)

TMP_IMG = 'tmp.jpg'

def allowed_file(filename):
  return '.' in filename and \
         filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

class Objects(object):
  def __init__(self):
    super().__init__()

  @staticmethod
  def get_objects_by_user_image_file(file):
    search = Search(log)

    res = GetObjectsResponse()

    if file and allowed_file(file.filename):
      im = PIL.Image.open(file.stream)
      format = im.format
      log.debug(im.format)

      try:
        if 'gif' == format.lower():
          log.debug('gif')
          im.seek(0)
          mypalette = im.getpalette()
          im.putpalette(mypalette)
          new_im = PIL.Image.new("RGBA", im.size)
          new_im.paste(im)
          new_im.save('foo' + '.png')

          bg = PIL.Image.new("RGB", im.size, (255,255,255))
          bg.paste(new_im, (0,0), new_im)
          bg.save(TMP_IMG, quality=95)
          im = bg

        elif 'png' == format.lower():
          log.debug('png')
          bg = PIL.Image.new("RGB", im.size, (255,255,255))
          bg.paste(im, im)
          bg.save(TMP_IMG, quality=95)
          im = bg
        else:
          im.save(TMP_IMG)

        userImage = {}
        image_url = utils.save_image_to_storage(str(uuid.uuid4()), 'user', TMP_IMG)

        boxes, objects = search.get_objects(TMP_IMG)
        images = search.search_image_file(TMP_IMG)

        user_api = Users()

        box_dic_list = []
        obj_ids = []
        i = 0
        for box in boxes:
          b = box.to_dict()
          b['feature'] = objects[i]['feature']
          box_dic_list.append(b)
          object_id = user_api.add_object('bluehackmaster', b)
          box.id = object_id
          obj_ids.append(object_id)
          rconn.hset(REDIS_USER_OBJECT_HASH, object_id, pickle.dumps(b))
          rconn.lpush(REDIS_USER_OBJECT_QUEUE, object_id)
          i = i + 1

        userImage['boxes'] = box_dic_list
        userImage['url'] = image_url

        image_id = user_api.add_image('bluehackmaster', userImage)

        userImage['device_id'] = 'bluehackmaster'
        userImage['image_id'] = image_id
        userImage.pop('boxes')
        userImage['objects'] = obj_ids

        rconn.lpush(REDIS_LOG_SEARCH_IMAGE_FILE_QUEUE, pickle.dumps(userImage))

        res_data = GetObjectsResponseData()
        res_data.boxes = boxes
        res_data.image_id = image_id
        images_list = []

        if images is None:
          res.message = "Successful, but there is no similar images"
          res_data.images = None
        else:
          for image in images:
            images_list.append(Image().from_dict(image))
          res.message = "Successful"
          res_data.images = images_list
        res.data = res_data
        response_status = 200

      except Exception as e:
        log.error(str(e))
        response_status = 400

      return res, response_status

  @staticmethod
  def get_objects_by_user_image_id(image_id):
    search = Search(log)
    res = GetObjectsByImageIdResponse()

    try:
      res_data = GetObjectsResponseData()
      boxes = search.get_objects_by_image_id(image_id)
      res_data.image_id = image_id
      res_data.boxes = boxes
      res.message = "Successful"
      res.data = res_data
      response_status = 200

    except Exception as e:
      log.error(str(e))
      response_status = 400

    return res, response_status

  @staticmethod
  def get_objects_by_image_id(image_id):
    search = Search(log)
    res = GetObjectsByImageIdResponse()

    try:
      image_d = rconn.hget(REDIS_INDEXED_IMAGE_HASH, image_id)
      if image_d != None:
        image = pickle.loads(image_d)
      else:
        image = search.get_indexed_image(image_id)

      boxes_array = []
      if image is not None:
        objects = image.get('objects')

        if objects is not None:
          for object in objects:
            object['id'] = str(object['_id'])
            boxes_array.append(BoxObject.from_dict(object))

      rconn.hset(REDIS_INDEXED_IMAGE_HASH, image_id, pickle.dumps(image))

      res_data = GetObjectsResponseData()
      res_data.boxes = boxes_array

      images = image.get('images')
      images_list = []
      if images is None:
        res.message = "Successful, but there is no similar images"
        res_data.images = None
      else:
        for image in images:
          images_list.append(Image().from_dict(image))
        res.message = "Successful"
        res_data.images = images_list

      res.data = res_data
      response_status = 200

    except Exception as e:
      log.error(str(e))
      response_status = 400

    return res, response_status
