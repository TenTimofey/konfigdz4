import csv
import sys
import struct

COMMANDS = {
    "LOAD_CONST": 3,
    "READ_MEM": 4,
    "WRITE_MEM": 6,
    "MIN": 0,
}


def assemble(input_file, output_file, log_file):
    with open(input_file, 'r') as infile, open(output_file, 'wb') as outfile, open(log_file, 'w',
                                                                                   newline='') as logfile:
        csv_writer = csv.writer(logfile)
        csv_writer.writerow(["instruction", "value"])

        for line in infile:
            parts = line.strip().split()
            cmd = parts[0]
            args = list(map(int, parts[1:]))

            if cmd == "LOAD_CONST":
                opcode = (COMMANDS[cmd] << 5) | ((args[0] >> 16) & 0x1F)
                operand = args[0] & 0xFFFF
                outfile.write(struct.pack(">BH", opcode, operand))
                csv_writer.writerow([cmd, args[0]])

            elif cmd == "READ_MEM":
                opcode = (COMMANDS[cmd] << 5) | ((args[0] >> 8) & 0x1F)
                operand = args[0] & 0xFF
                outfile.write(struct.pack(">BB", opcode, operand))
                csv_writer.writerow([cmd, args[0]])

            elif cmd == "WRITE_MEM":
                opcode = COMMANDS[cmd] << 5
                outfile.write(struct.pack(">B", opcode))
                csv_writer.writerow([cmd, None])

            elif cmd == "MIN":
                opcode = COMMANDS[cmd] << 5
                address = args[0]
                outfile.write(struct.pack(">BH", opcode, address))
                csv_writer.writerow([cmd, args[0]])