## This module provides an RFC4122 compliant UUIDv4 generator
import std/sysrand
import std/sequtils
import strutils

proc uuid(): string =
  ## This function returns a randomized UUIDv4
  var b = urandom(16)
  b[6] = (b[6] and 0x0F) or 0x40
  b[8] = (b[8] and 0x3F) or 0x80
  result = (b[0..3].mapIt(toHex(it, 2)).join("") & "-" &
           b[4..5].mapIt(toHex(it, 2)).join("") & "-" &
           b[6..7].mapIt(toHex(it, 2)).join("") & "-" &
           b[8..9].mapIt(toHex(it, 2)).join("") & "-" &
           b[10..15].mapIt(toHex(it, 2)).join("")).toLowerAscii 

export uuid