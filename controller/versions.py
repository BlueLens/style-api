from bson.objectid import ObjectId
from controller.database import DataBase

from swagger_server.models.version import Version
from swagger_server.models.add_version_response import AddVersionResponse
from swagger_server.models.add_version_response_data import AddVersionResponseData

from swagger_server.models.get_version_response import GetVersionResponse


class Versions(DataBase):
  def __init__(self):
    super().__init__()
    self.versions = self.db.versions

  @staticmethod
  def add_version(connexion):
    orm = Versions()
    res = AddVersionResponse()
    data = AddVersionResponseData()
    response_status = 200

    if connexion.request.is_json:
      version = Version.from_dict(connexion.request.get_json())

      try:
        r = orm.versions.insert(version.to_dict())
        res.message = 'Successfully added'
        data.version_id = str(r)
        res.data = data
      except Exception as e:
        res.message = str(e)
        response_status = 400

    return res, response_status

  @staticmethod
  def get_version_by_id(version_id):
    orm = Versions()
    res = GetVersionResponse()
    response_status = 200

    try:
      r = orm.versions.find_one({"_id": ObjectId(version_id)})
      res.message = 'Successful'
      version = Version.from_dict(r)
      version.id = str(r['_id'])
      version.created_at = r['_id'].generation_time
      res.data = version.to_dict()
    except Exception as e:
      res.message = str(e)
      response_status = 400

    return res, response_status
