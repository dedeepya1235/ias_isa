from assembler import IASAssembler
from processor import IASProcessor


def main():
    assembler = IASAssembler()
    machine_code = assembler.assemble("./eg1.txt")
    print(machine_code)


main()
