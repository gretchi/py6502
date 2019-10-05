#!/usr/bin/env python3

import sys

from mos6502 import opcodes

ADDR_MODE_ACCUMULATOR   = 0x01
ADDR_MODE_RELATIVE      = 0x02
ADDR_MODE_ABSOLUTE      = 0x03
ADDR_MODE_ABSOLUTE_Y    = 0x04
ADDR_MODE_ABSOLUTE_X    = 0x05
ADDR_MODE_IMMEDIATE     = 0x06
ADDR_MODE_IMPLIED       = 0x07
ADDR_MODE_INDIRECT      = 0x08
ADDR_MODE_INDIRECT_X    = 0x09
ADDR_MODE_INDIRECT_Y    = 0x0A
ADDR_MODE_ZEROPAGE      = 0x0B
ADDR_MODE_ZEROPAGE_X    = 0x0C
ADDR_MODE_ZEROPAGE_Y    = 0x0D

MEM_MAP_ROM_LOW_BEGIN   = 0x8000
MEM_MAP_ROM_LOW_END     = 0xBFFF


def main():
    asm_path = sys.argv[1]

    asm_bin = None

    with open(asm_path, "rb") as fh:
        asm_bin = fh.read()


    is_reading_operand = False
    program_counter = 0x0000
    relative_program_counter = MEM_MAP_ROM_LOW_BEGIN

    while True:
        if program_counter < len(asm_bin):
            opcode = asm_bin[program_counter + 0x0010]

        if relative_program_counter >= MEM_MAP_ROM_LOW_END:
            break


        instruction, addr_mode, length, cycle, symbol = opcodes[opcode]

        if instruction is None:
            program_counter += 1
            continue

        opcode_operands = []

        for offset in range(length):
            opcode_operands.append(asm_bin[program_counter + 0x0010 + offset])


        operands = []

        for offset in range(length - 1):
            operands.append(asm_bin[program_counter + 0x0010 + offset + 1])

        relative_program_counter = program_counter + MEM_MAP_ROM_LOW_BEGIN

        sys.stdout.write(f"${relative_program_counter:04X}\t")


        for i in range(3):
            if len(opcode_operands) > i:
                sys.stdout.write(f"{opcode_operands[i]:02X} ")
            else:
                sys.stdout.write(f"   ")

        sys.stdout.write(f"   {symbol}    ")

        if operands:
            if addr_mode == ADDR_MODE_IMMEDIATE:
                # Immediate
                sys.stdout.write(f"#")

            if addr_mode in (ADDR_MODE_INDIRECT, ADDR_MODE_INDIRECT_X, ADDR_MODE_INDIRECT_Y):
                sys.stdout.write(f"(")

            sys.stdout.write(f"$")
        for operand in reversed(operands):
            if addr_mode == ADDR_MODE_RELATIVE:
                absolute_addr = relative_program_counter + signed_int8(operand) + length
                sys.stdout.write(f"{absolute_addr:02X}")

            else:
                sys.stdout.write(f"{operand:02X}")

        if addr_mode in (ADDR_MODE_ABSOLUTE_X, ADDR_MODE_ZEROPAGE_X, ADDR_MODE_INDIRECT_X):
            sys.stdout.write(f", X")

        if addr_mode in (ADDR_MODE_ABSOLUTE_Y, ADDR_MODE_ZEROPAGE_Y, ADDR_MODE_INDIRECT_Y):
            sys.stdout.write(f", Y")

        if addr_mode in (ADDR_MODE_INDIRECT, ADDR_MODE_INDIRECT_X, ADDR_MODE_INDIRECT_Y):
            sys.stdout.write(f")")

        sys.stdout.write(f"\n")

        program_counter += length


def signed_int8(value):
    return -(value & 0b10000000) | (value & 0b01111111)


if __name__ == "__main__":
    main()
