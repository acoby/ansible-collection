def quote_wrap(arg):
  if arg is None:
    return None
  return [ '"' + x + '"' for x in arg]

class FilterModule(object):
  def filters(self):
    return {'quote_wrap': quote_wrap}
