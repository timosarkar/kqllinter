## This module implements 12bit IETF chacha20.
proc xorbytes(a, b: seq[byte]): seq[byte] =
  result = newSeq[byte](a.len)
  for i in 0..<a.len:
    result[i] = a[i] xor b[i]

proc rotl(x: int, n: int): int =
  return (x shl n) or (x shr (32-n))

proc qr(a: int, b: int, c: int, d: int): tuple[a,b,c,d: int] =
  var aa = a; var bb = b; var cc = c; var dd = d
  aa = (aa + bb) and 0xffffffff; dd = dd xor aa; dd = rotl(dd,16)
  cc = (cc + dd) and 0xffffffff; bb = bb xor cc; bb = rotl(bb,12)
  aa = (aa + bb) and 0xffffffff; dd = dd xor aa; dd = rotl(dd,8)
  cc = (cc + dd) and 0xffffffff; bb = bb xor cc; bb = rotl(bb,7)
  return (aa, bb, cc, dd)

proc bytesToInts(b: seq[byte]): seq[int] =
  result = @[]
  for i in countup(0, b.len-4, 4):
    result.add(int(b[i]) or (int(b[i+1]) shl 8) or (int(b[i+2]) shl 16) or (int(b[i+3]) shl 24))

proc intsToBytes(ints: seq[int]): seq[byte] =
  result = @[]
  for x in ints:
    result.add(byte(x and 0xff))
    result.add(byte((x shr 8) and 0xff))
    result.add(byte((x shr 16) and 0xff))
    result.add(byte((x shr 24) and 0xff))

proc chacha20(key: seq[byte], counter: int, nonce: seq[byte]): seq[byte] =
  #[
  
  ]#
  
  let k = bytesToInts(key)
  let n = bytesToInts(nonce)
  var state = @[0x61707865, 0x3320646e, 0x79622d32, 0x6b206574] & k & @[counter] & n
  var w = state
  for _ in 0..9:
    (w[0], w[4], w[8], w[12]) = qr(w[0], w[4], w[8], w[12])
    (w[1], w[5], w[9], w[13]) = qr(w[1], w[5], w[9], w[13])
    (w[2], w[6], w[10], w[14]) = qr(w[2], w[6], w[10], w[14])
    (w[3], w[7], w[11], w[15]) = qr(w[3], w[7], w[11], w[15])
    (w[0], w[5], w[10], w[15]) = qr(w[0], w[5], w[10], w[15])
    (w[1], w[6], w[11], w[12]) = qr(w[1], w[6], w[11], w[12])
    (w[2], w[7], w[8], w[13]) = qr(w[2], w[7], w[8], w[13])
    (w[3], w[4], w[9], w[14]) = qr(w[3], w[4], w[9], w[14])
  for i in 0..15:
    w[i] = (w[i] + state[i]) and 0xffffffff
  intsToBytes(w)

export chacha20