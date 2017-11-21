
from bson.objectid import ObjectId
from orm.database import DataBase
from swagger_server.models.object import Object
from swagger_server.models.add_object_response import AddObjectResponse
from swagger_server.models.add_object_response_data import AddObjectResponseData
from swagger_server.models.get_object_response import GetObjectResponse


class Objects(DataBase):
  def __init__(self):
    super().__init__()
    self.objects = self.db.objects

  @staticmethod
  def add_object(connexion):
    orm = Objects()
    res = AddObjectResponse()
    data = AddObjectResponseData()
    response_status = 200
    if connexion.request.is_json:
      body = Object.from_dict(connexion.request.get_json())

      try:
        r = orm.objects.insert(body.to_dict())
        res.message = 'Successful'
        data.object_id = str(r)
        res.data = data
      except Exception as e:
        res.message = str(e)
        response_status = 400

    return res, response_status

  @staticmethod
  def get_object_by_id(object_id):
    print('get_object')
    orm = Objects()
    res = GetObjectResponse()
    response_status = 200

    try:
      r = orm.objects.find_one({"_id": ObjectId(object_id)})
      res.message = 'Successful'
      object = Object.from_dict(r)
      object.id = str(r['_id'])
      res.data = object.to_dict()
    except Exception as e:
      res.message = str(e)
      response_status = 400

    return res, response_status

