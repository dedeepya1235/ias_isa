class IAS_processor:
    def __init__(self, file_name):
        self.PC = 0b0000_0000_0000
        self.AC = 0b0000_0000_0000_0000_0000_0000_0000_0000_0000_0000
        self.IR = 0b0000_0000
        self.MAR = 0b0000_0000_0000
        self.MBR = 0b0000_0000_0000_0000_0000_0000_0000_0000_0000_0000
        self.IBR = 0b0000_0000_0000_0000_0000
        self.MQ = 0b0000_0000_0000_0000_0000_0000_0000_0000_0000_0000
        self.M = {}

        with open(file_name, "r") as file:
            lines = file.readlines()
            for line in lines:
                line = line.strip()
                x = line.split(" ")
                x[0] = int(x[0], 2)
                x[1] = int(x[1], 2)
                self.M[x[0]] = x[1]

        self.fetch_cycle()

    def fetch_cycle(self):
        self.MAR = self.PC
        self.MBR = self.M[self.MAR]
        self.PC += 1
        self.decode_cycle()

    def decode_cycle(self):
        left_instruction = self.MBR >> 20
        right_instruction = self.MBR & 0b1111_1111_1111_1111_1111
        self.IR = left_instruction >> 12
        self.MAR = left_instruction & 0b1111_1111_1111
        self.IBR = right_instruction
        self.execute_cycle()

    def execute_cycle(self):
        # Data transfer instructions
        if self.IR == 0b0000_1010:
            self.AC = self.MQ  # implement LOAD MQ

        elif self.IR == 0b0000_1001:
            # MAR would have address of X
            self.MBR = self.M[self.MAR]
            self.MQ = self.MBR  # implement LOAD MQ,M(X)

        elif self.IR == 0b0010_0001:
            self.MBR = self.AC
            self.M[self.MAR] = self.MBR  # implement STOR M(X)

        elif self.IR == 0b0000_0001:
            self.MBR = self.M[self.MAR]
            self.AC = self.MBR

        elif self.IR == 0b0000_0010:
            self.MBR = self.M[self.MAR]
            self.AC = -self.MBR

        elif self.IR == 0b0000_0011:
            self.MBR = self.M[self.MAR]
            self.AC = abs(self.MBR)

        elif self.IR == 0b0000_0100:
            self.MBR = self.M[self.MAR]
            self.AC = -abs(self.MBR)

        # Unconditional branch instructions
        elif self.IR == 0b0000_1101:
            # pass  # implement JUMP M(X,0:19)
            self.PC = self.MAR

        elif self.IR == 0b0000_1110:
            # pass  # implement JUMP M(X,20:39)
            self.PC = self.MAR
            self.MBR = self.M[self.MAR] & 0b1111_1111_1111_1111_1111
            self.IR = self.MBR >> 12
            self.MAR = self.MBR & 0b1111_1111_1111

        # Conditional branch instructions
        elif self.IR == 0b0000_1111:
            pass  # implement JUMP+ M(X,0:19)

        elif self.IR == 0b0001_0000:
            pass  # implement JUMP+ M(X,20:39)

        # Arithmetic instructions
        elif self.IR == 0b0000_0101:
            pass  # implement ADD M(X)

        elif self.IR == 0b0000_0111:
            pass  # implement ADD |M(X)|

        elif self.IR == 0b0000_0110:
            pass  # implement SUB M(X)

        elif self.IR == 0b0000_1000:
            pass  # implement SUB |M(X)|

        elif self.IR == 0b0000_1011:
            pass  # implement MUL M(X)

        elif self.IR == 0b0000_1100:
            pass  # implement DIV M(X)

        elif self.IR == 0b0001_0100:
            # pass  # implement LSH
            self.AC <<= 1

        elif self.IR == 0b0001_0101:
            # pass  # implement RSH
            self.AC >>= 1

        # Adress modify instructions
        elif self.IR == 0b0001_0010:
            pass  # implement STOR M(X,8:19)

        elif self.IR == 0b0001_0011:
            pass  # implement STOR M(X,28:39)

        if self.IBR:
            self.IR = self.IBR >> 12  # Getting the first 8bits ie opcode
            self.MAR = self.IBR & 0b1111_1111_1111  # Getting the last 12bits for adress

            self.IBR = 0b0000_0000_0000_0000_0000  # resetting IBR after it's use

            self.execute_cycle()

        else:
            self.fetch_cycle()


a = IAS_processor("machine_code.txt")
