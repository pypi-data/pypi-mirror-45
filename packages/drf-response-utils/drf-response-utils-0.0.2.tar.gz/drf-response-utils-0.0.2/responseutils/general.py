from rest_framework.response import Response
from rest_framework import status

class General:

  @classmethod
  def success(cls, message):
    data = {
      "Success":True,
      "Message":message
    }
    status_code = status.HTTP_200_OK

    return Response(data, status=status_code)
  
  @classmethod
  def success_data(cls, data):
    data = {
      "Success":True,
      "Data":data
    }
    status_code = status.HTTP_200_OK

    return Response(data, status=status_code)
  
  @classmethod
  def created(cls, data):
    data = {
      "Success":True,
      "Data":data
    }
    status_code = status.HTTP_201_CREATED

    return Response(data, status=status_code)
  
  @classmethod
  def fail(cls, message):
    data = {
      "Success":False,
      "Message":message
    }
    status_code = status.HTTP_400_BAD_REQUEST

    return Response(data, status=status_code)
  
  @classmethod
  def not_found(cls, message):
    data = {
      "Success":False,
      "Message":message
    }
    status_code = status.HTTP_404_NOT_FOUND

    return Response(data, status=status_code)