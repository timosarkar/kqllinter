import crypto/keys
import crypto/chacha20

let key = newkey(32)
let nonce = newkey(12)
let plaintext = "Hello NimChaCha20!"
var counter = 0
var offset = 0

while offset < plaintext.len:
  let block2 = chacha20(key, counter, nonce)
  let blockSize = min(64, plaintext.len - offset)
  echo $block2