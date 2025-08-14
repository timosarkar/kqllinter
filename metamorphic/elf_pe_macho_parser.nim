import std/streams

# nim c -r b.nim
proc isElf(path: string): bool =
  var fs = newFileStream(path)
  var magic: array[4, byte]
  discard fs.readBytes(magic.toOpenArray(0, 3))

  return magic == [byte(0x7F), byte('E'), byte('L'), byte('F')]

isElf("./a")
