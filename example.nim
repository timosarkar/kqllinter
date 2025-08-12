# example.nim
import strformat
include "capstone"  # Include the bindings file

proc disassemble_x86_64() =
  var handle: csh
  
  # Initialize Capstone for x86-64
  let err = cs_open(CS_ARCH_X86, CS_MODE_64, addr handle)
  if err != CS_ERR_OK:
    echo "Failed to initialize Capstone: ", cs_strerror(err)
    return
  
  # Sample x86-64 machine code: mov eax, 1; ret
  let code: array[6, uint8] = [0xb8u8, 0x01, 0x00, 0x00, 0x00, 0xc3]
  let address: uint64 = 0x1000
  
  var insn: ptr cs_insn
  
  # Disassemble the code
  let count = cs_disasm(handle, unsafeAddr code[0], code.len.csize_t, address, 0, addr insn)
  
  if count > 0:
    echo "Disassembling x86-64 code:"
    echo "=========================="
    
    for i in 0..<count:
      let inst = cast[ptr cs_insn](cast[int](insn) + int(i) * sizeof(cs_insn))[]
      echo &"0x{inst.address:08x}: {inst.getMnemonic()} {inst.getOpStr()}"
    
    # Free allocated memory
    cs_free(insn, count)
  else:
    echo "Failed to disassemble code"
  
  # Clean up
  discard cs_close(addr handle)

proc disassemble_arm64() =
  var handle: csh
  
  # Initialize Capstone for ARM64
  let err = cs_open(CS_ARCH_ARM64, CS_MODE_ARM, addr handle)
  if err != CS_ERR_OK:
    echo "Failed to initialize Capstone: ", cs_strerror(err)
    return
  
  # Sample ARM64 machine code: mov x0, #1; ret
  let code: array[8, uint8] = [0x20u8, 0x00, 0x80, 0xd2, 0xc0, 0x03, 0x5f, 0xd6]
  let address: uint64 = 0x2000
  
  var insn: ptr cs_insn
  
  # Disassemble the code
  let count = cs_disasm(handle, unsafeAddr code[0], code.len.csize_t, address, 0, addr insn)
  
  if count > 0:
    echo "\nDisassembling ARM64 code:"
    echo "========================="
    
    for i in 0..<count:
      let inst = cast[ptr cs_insn](cast[int](insn) + int(i) * sizeof(cs_insn))[]
      echo &"0x{inst.address:08x}: {inst.getMnemonic()} {inst.getOpStr()}"
    
    # Free allocated memory
    cs_free(insn, count)
  else:
    echo "Failed to disassemble code"
  
  # Clean up
  discard cs_close(addr handle)

proc show_version() =
  var major, minor: cint
  let version = cs_version(addr major, addr minor)
  echo &"Capstone version: {major}.{minor} (lib version: {version})"

when isMainModule:
  show_version()
  disassemble_x86_64()
  disassemble_arm64()
