from assembler import IASAssembler
from IAS_processor import IAS_processor

# need to change the assembler so that instead of -00000001100 it gives the twos complement


def main():
    assembler = IASAssembler()
    machine_code = assembler.assemble("./eg1.txt", "./machine_code.txt")
    # print(machine_code)


main()
