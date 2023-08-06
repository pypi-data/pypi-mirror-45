# encoding:utf-8 
import socket 
from   contextlib import closing
import ctypes

def check_service(ip, port):
  """
  检测服务器端口是否开放
  """
  with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as sock:
    if sock.connect_ex((ip, port)) == 0:
      return True  # OPEN
    else:
      return False # closed
      
class Base(ctypes.Structure):

  def _to_str(self, value):
    """
    :return:
    """
    if isinstance(value, str):
      return value 
    else:
      return str(value)
      
  def _to_str4where(self, value):
    """
    :return:
    """
    if isinstance(value, str):
      return "'" + value + "'"
    else:
      return str(value)

  def _to_bytes(self, value):
    """
    :return:
    """
    if isinstance(value, bytes):
      return value
    else:
      return bytes(str(value), encoding="utf-8")

  @classmethod
  def from_dict(cls, obj):
    """
    :return:
    """
    return cls(**obj)

  def to_dict(self):
    """
    :return:
    """
    results = {}
    for key, _ in self._fields_:
      _value = getattr(self, key)
      if isinstance(_value, bytes):
        results[key] = _value.decode(encoding="gb18030", errors="ignore")
      else:
        results[key] = _value
    return results

  def __repr__(self):
    """
    :return:
    """
    items = ["%s:%s" % (item, getattr(self, item)) for item, value in self._fields_]
    return  "%s<%s>" % (self.__class__.__name__, ",".join(items))
