import struct

elf_path = 'a'

with open(elf_path, 'rb') as f:
    # Read ELF header (64 bytes)
    elf_header = f.read(64)

    # Check magic number
    if elf_header[:4] != b'\x7fELF':
        raise ValueError("Not an ELF file")

    # Only handle 64-bit little-endian
    if elf_header[4] != 2 or elf_header[5] != 1:
        raise ValueError("Only 64-bit little-endian ELF supported")

    # Parse ELF header
    e_shoff = struct.unpack_from('<Q', elf_header, 40)[0]  # section header offset
    e_shentsize = struct.unpack_from('<H', elf_header, 58)[0]  # size of section header
    e_shnum = struct.unpack_from('<H', elf_header, 60)[0]  # number of sections
    e_shstrndx = struct.unpack_from('<H', elf_header, 62)[0]  # section header string table index

    # Read section header string table
    f.seek(e_shoff + e_shentsize * e_shstrndx)
    sh = f.read(e_shentsize)
    sh_name, sh_type, sh_flags, sh_addr, sh_offset, sh_size, sh_link, sh_info, sh_addralign, sh_entsize = struct.unpack('<IIQQQQIIQQ', sh)

    f.seek(sh_offset)
    shstrtab = f.read(sh_size)

    # Iterate all section headers
    for i in range(e_shnum):
        f.seek(e_shoff + i * e_shentsize)
        sh = f.read(e_shentsize)
        sh_name, sh_type, sh_flags, sh_addr, sh_offset, sh_size, sh_link, sh_info, sh_addralign, sh_entsize = struct.unpack('<IIQQQQIIQQ', sh)
        # Get section name
        name = b''
        idx = sh_name
        while shstrtab[idx] != 0:
            name += bytes([shstrtab[idx]])
            idx += 1
        section_name = name.decode()
        if section_name == '.text':
            print(f".text section found at file offset: {hex(sh_offset)}")
            print(f".text section virtual address: {hex(sh_addr)}")
            print(f".text section size: {hex(sh_size)}")
            break
