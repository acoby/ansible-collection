import urllib

def urlencode_filter(arg):
  if arg is None:
    return None
  arg = arg.encode('utf8','ignore')
  return urllib.parse.quote_plus(arg)  

class FilterModule(object):
  def filters(self):
    return {'urlencode': urlencode_filter}
