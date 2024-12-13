import csv
import struct
import sys

class VirtualMachine:
    def __init__(self, memory_size=1024):
        self.stack = []
        self.memory = [0] * memory_size

    def execute(self, program, output_file, memory_range):
        with open(output_file, 'w', newline='') as outfile:
            csv_writer = csv.writer(outfile)
            csv_writer.writerow(["address", "value"])

            pc = 0
            while pc < len(program):
                opcode = program[pc] >> 5
                if opcode == 3:  # LOAD_CONST
                    const = ((program[pc] & 0x1F) << 16) | struct.unpack(">H", program[pc+1:pc+3])[0]
                    self.stack.append(const)
                    pc += 3
                elif opcode == 4:  # READ_MEM
                    offset = program[pc] & 0x1F
                    address = self.stack.pop() + offset
                    self.stack.append(self.memory[address])
                    pc += 2
                elif opcode == 6:  # WRITE_MEM
                    value = self.stack.pop()
                    address = self.stack.pop()
                    self.memory[address] = value
                    pc += 1
                elif opcode == 0:  # MIN
                    address = struct.unpack(">H", program[pc+1:pc+3])[0]
                    value = min(self.memory[address], self.stack.pop())
                    self.stack.append(value)
                    pc += 3
                else:
                    raise ValueError(f"Unknown opcode: {opcode}")

            # Сохраняем диапазон памяти
            for addr in range(memory_range[0], memory_range[1] + 1):
                csv_writer.writerow([addr, self.memory[addr]])

def load_binary(file_path):
    with open(file_path, 'rb') as f:
        return f.read()