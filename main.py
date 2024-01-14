from assembler import IASAssembler
from IAS_processor import IAS_processor


def main():
    assembler = IASAssembler()
    machine_code = assembler.assemble("./eg1.txt", "./machine_code.txt")
    processor = IAS_processor(
        1,
        50,
        "./machine_code.txt",
    )
    print(processor.AC)


main()
