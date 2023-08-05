import operator

def bsearch(a, v, lo=0, hi=None, key=lambda x: x, op=operator.lt):
  """return smallest i such that NOT op(a[i], v)"""
  if hi is None:
    hi = len(a)
  while lo < hi:
    mid = (lo+hi)//2
    midval = key(a[mid])
    if op(midval, v):
      lo = mid+1
    else:
      hi = mid
  
  return lo

def bisect_left(a, v, lo=0, hi=None, key=lambda x: x):
  """return the smallest i such that NOT a[i] < v"""
  op = operator.lt
  return bsearch(a, v, lo, hi, key, op)

def bisect_right(a, v, lo=0, hi=None, key=lambda x: x):
  """return the smallest i such that NOT a[i] <= v"""
  op = operator.le
  return bsearch(a, v, lo, hi, key, op)