
class IASAssembler:
    def __init__(self, path, out):
        # Dictionary contains the opcode for the possible instructions in assembly code
        self.instructions = {
            "LOAD_MQ": "00001010",
            "LOAD_MQ_M_X": "00001001",
            "STOR_M_X": "00100001",
            "LOAD_M_X": "00000001",
            "LOAD_NEG_M_X": "00000010",
            "LOAD_ABS_M_X": "00000011",
            "LOAD_NEG_ABS_M_X": "00000100",
            "JUMP_M_X_0_19": "00001101",
            "JUMP_M_X_20_39": "00001110",
            "JUMP_POS_M_X_0_19": "00001111",
            "JUMP_POS_M_X_20_39": "00010000",
            "ADD_M_X": "00000101",
            "ADD_ABS_M_X": "00000111",
            "SUB_M_X": "00000110",
            "SUB_ABS_M_X": "00001000",
            "MUL_M_X": "00001011",
            "DIV_M_X": "00001100",
            "LSH": "00010100",
            "RSH": "00010101",
            "STOR_M_X_8_19": "00010010",
            "STOR_M_X_28_39": "00010011",
            "NOP": "00011100",
            "INCR_AC": "00100000",
            "DECR_AC": "00100010"
        }
        
        self.path = path
        self.out = out
        
        self.assemble()

    # We want the machine code in format 12-bit address + ' ' + 40-bit memory location
    def assemble(self):
        # c keeps track of the line address
        c = 0

        with open(self.path, "r") as source, open(self.out, "w") as output:
            for line in source:
                c += 1
                # Allows us to add comments in the assembly code by using #
                if line.startswith("#"):
                    continue

                line = line.split("#")[0].strip()

                if line:
                    instructions = line.strip().split()
                    first = instructions[0]

                    temp1 = format(c, "012b") + " "
                    temp2 = ""

                    if self.instructions.get(first):
                        for instruction in instructions:
                            opcode = self.instructions.get(instruction)

                            if opcode:
                                # if the instructions are LOAD MQ, NOP, INCR or DECR
                                # Since they don't need an address, we add 12-0-bits behind it
                                if opcode in {"00001010", "00011100", "00100000", "00100010"}:
                                    temp2 += opcode
                                    temp2 += format(0, "012b")
                                else:
                                    temp2 += opcode

                            else:
                                temp2 += format(int(instruction), "012b")

                    else:
                        if int(first) >= 0:
                            temp2 += format(int(first), "040b")
                        # If the number is negative, this converts it to two's compliment form
                        else:
                            temp2 += format(int(first) & 0b111111111111, "040b")

                    if len(temp2) < 40:
                        temp2 += "0" * (40 - len(temp2))
                    # Finally the program writes the machine code line by line and saves it in output file
                    output.write(temp1 + temp2 + "\n")
