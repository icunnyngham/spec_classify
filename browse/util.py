def colormap(normValue):
  """ Takes a value normalized to 1, and spits out a hex color code for a linear b&w colormap """
  v = normValue*255
  return "#%02x%02x%02x" % (v, v, v)
