class FilterModule(object):
  def filters(self):
    return {
      'service_ipv4_address': self.service_ipv4_address,
      'service_ipv6_address': self.service_ipv6_address,
    }
  
  def service_ipv4_address(self, instancePort, basePort, shortRange = False):
    if shortRange:
      bnet = int(basePort/100)
      cnet = int(basePort/10) - (int(basePort/100)*10)
      dnet = (instancePort % basePort)*16
      mask = 28
    else:
      bnet = int(basePort/100)
      cnet = instancePort % basePort
      dnet = 0
      mask = 24
    
    if bnet < 0 or bnet > 255:
      bnet = 0
    
    if cnet < 0 or cnet > 255:
      cnet = 0
      
    if dnet < 0 or dnet > 255:
      dnet = 0

    return '172.' + str(bnet) + '.' +str(cnet)+ '.' +str(dnet)+ '/' + str(mask)

  def service_ipv6_address(self, instancePort, basePort, shortRange = False):
    bnet = basePort
    cnet = format(instancePort % basePort, 'x')
    mask = 110
    
    return 'fc00:ac0b:0:0:' + str(bnet) + ':' + str(cnet) + '::/' + str(mask)

