#[
import std/[asyncdispatch, httpclient]

proc asyncProc(): Future[string] {.async.} =
  var client = newAsyncHttpClient()
  try:
    return await client.getContent("http://google.com")
  finally:
    client.close()

echo waitFor asyncProc()
]#

# nim c -d:release --opt:speed implant.nim
import uuids
import std/httpclient
var client = newHttpClient()
try:
  echo client.getContent("http://google.com")
finally:
  client.close()
