import random

## This function generates a random 256bit key
proc newkey(n: int): seq[byte] =
  result = newSeq[byte](n)
  for i in 0..<n:
    result[i] = rand(byte)
  return result

export newkey