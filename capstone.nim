{.pragma: cs, dynlib: "libcapstone".}

type
  cs_arch* = enum
    CS_ARCH_ARM = 0
    CS_ARCH_ARM64 = 1
    CS_ARCH_MIPS = 2
    CS_ARCH_X86 = 3
    CS_ARCH_PPC = 4
    CS_ARCH_SPARC = 5
    CS_ARCH_SYSZ = 6
    CS_ARCH_XCORE = 7
    CS_ARCH_M68K = 8
    CS_ARCH_TMS320C64X = 9
    CS_ARCH_M680X = 10
    CS_ARCH_EVM = 11
    CS_ARCH_MOS65XX = 12
    CS_ARCH_WASM = 13
    CS_ARCH_BPF = 14
    CS_ARCH_RISCV = 15
    CS_ARCH_SH = 16
    CS_ARCH_TRICORE = 17
    CS_ARCH_MAX = 18
    CS_ARCH_ALL = 0xFFFF

  cs_err* = enum
    CS_ERR_OK = 0
    CS_ERR_MEM = 1
    CS_ERR_ARCH = 2
    CS_ERR_HANDLE = 3
    CS_ERR_CSH = 4
    CS_ERR_MODE = 5
    CS_ERR_OPTION = 6
    CS_ERR_DETAIL = 7
    CS_ERR_MEMSETUP = 8
    CS_ERR_VERSION = 9
    CS_ERR_DIET = 10
    CS_ERR_SKIPDATA = 11
    CS_ERR_X86_ATT = 12
    CS_ERR_X86_INTEL = 13
    CS_ERR_X86_MASM = 14

# Using constants instead of enum to avoid duplicate values
const
  CS_MODE_LITTLE_ENDIAN* = 0
  CS_MODE_ARM* = 0
  CS_MODE_16* = 1 shl 1
  CS_MODE_32* = 1 shl 2  
  CS_MODE_64* = 1 shl 3
  CS_MODE_THUMB* = 1 shl 4
  CS_MODE_MCLASS* = 1 shl 5
  CS_MODE_V8* = 1 shl 6
  CS_MODE_BIG_ENDIAN* = 1 shl 31

type
  cs_mode* = cuint
  csh* = csize_t
  
  cs_insn* {.importc: "cs_insn", header: "<capstone/capstone.h>".} = object
    id*: cuint
    address*: uint64
    size*: uint16
    bytes*: array[24, uint8]
    mnemonic*: array[32, char]
    op_str*: array[160, char]

# Import functions with correct signatures from header
proc cs_open*(arch: cs_arch, mode: cs_mode, handle: ptr csh): cs_err {.importc, header: "<capstone/capstone.h>".}
proc cs_close*(handle: ptr csh): cs_err {.importc, header: "<capstone/capstone.h>".}
proc cs_disasm*(handle: csh, code: ptr uint8, code_size: csize_t, 
                address: uint64, count: csize_t, insn: ptr ptr cs_insn): csize_t {.importc, header: "<capstone/capstone.h>".}
proc cs_free*(insn: ptr cs_insn, count: csize_t) {.importc, header: "<capstone/capstone.h>".}
proc cs_errno*(handle: csh): cs_err {.importc, header: "<capstone/capstone.h>".}
proc cs_strerror*(code: cs_err): cstring {.importc, header: "<capstone/capstone.h>".}
proc cs_version*(major: ptr cint, minor: ptr cint): cuint {.importc, header: "<capstone/capstone.h>".}
proc cs_support*(query: cint): bool {.importc, header: "<capstone/capstone.h>".}

# Convenience wrappers
proc `$`*(insn: cs_insn): string =
  result = $cast[cstring](addr insn.mnemonic[0])
  let opstr = $cast[cstring](addr insn.op_str[0])
  if opstr.len > 0:
    result.add(" ")
    result.add(opstr)

proc getMnemonic*(insn: cs_insn): string =
  return $cast[cstring](addr insn.mnemonic[0])

proc getOpStr*(insn: cs_insn): string =
  return $cast[cstring](addr insn.op_str[0])