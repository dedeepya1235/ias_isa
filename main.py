from IAS_processor import IASprocessor
from IAS_assembler import IASAssembler

assembler = IASAssembler("./assembly_code.txt", "./machine_code.txt")

processor = IASprocessor(20, 50, "./machine_code.txt")
print(processor.M[1])
print(processor.M[2])
print(processor.M[3])
print(processor.M[4])
print(processor.M[5])
print(processor.M[6])
print(processor.M[7])
print(processor.M[8])
print(processor.M[9])
print(processor.M[10])