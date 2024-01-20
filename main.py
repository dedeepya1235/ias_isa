from IAS_processor import IASprocessor
from IAS_assembler import IASAssembler

assembler = IASAssembler("./assembly_code.txt", "./machine_code.txt")

processor = IASprocessor(20, 50, "./machine_code.txt")
print(a.M[1])
print(a.M[2])
print(a.M[3])
print(a.M[4])
print(a.M[5])
print(a.M[6])
print(a.M[7])
print(a.M[8])
print(a.M[9])
print(a.M[10])