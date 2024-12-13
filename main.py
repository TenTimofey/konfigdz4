import sys
from assembler import assemble
from interpreter import VirtualMachine, load_binary


def main():
    if len(sys.argv) < 5:
        print("Usage: python main.py <mode> <input> <output> <log/result>")
        sys.exit(1)

    mode = sys.argv[1]
    input_file = sys.argv[2]
    output_file = sys.argv[3]
    log_or_result = sys.argv[4]

    if mode == "assemble":
        assemble(input_file, output_file, log_or_result)
    elif mode == "interpret":
        memory_range = tuple(map(int, sys.argv[5:7]))
        program = load_binary(input_file)
        vm = VirtualMachine()
        vm.execute(program, log_or_result, memory_range)
    else:
        print("Invalid mode. Use 'assemble' or 'interpret'.")
        sys.exit(1)


if __name__ == "__main__":
    main()