import strformat
import "capstone"

proc disassemble_x86_64() =
  var handle: csh
  let err = cs_open(CS_ARCH_X86, CS_MODE_64, addr handle)
  let code: array[6, uint8] = [0xb8u8, 0x01, 0x00, 0x00, 0x00, 0xc3]
  let address: uint64 = 0x1000
  var insn: ptr cs_insn
  let count = cs_disasm(handle, unsafeAddr code[0], code.len.csize_t, address, 0, addr insn)
  
  if count > 0:
    for i in 0..<count:
      let inst = cast[ptr cs_insn](cast[int](insn) + int(i) * sizeof(cs_insn))[]
      echo &"0x{inst.address:08x}: {inst.getMnemonic()} {inst.getOpStr()}"
    cs_free(insn, count)
  discard cs_close(addr handle)

when isMainModule:
  disassemble_x86_64()