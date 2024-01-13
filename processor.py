class IASProcessor:
    def __init__(self, pc):
        self.AC = "00000000000000000000"
        self.MQ = "0000000000000 0000000"
        self.MBR = "00000000000000000000"
        self.MAR = "000000000000"
        self.IR = "00000000"
        self.IBR = "00000000000000000000"
        self.memory = [0] * 4096
        self.pc = pc

    def fetch(self):
        if self.IBR:
            self.IR = self.IBR[:8]
            self.MAR = self.IBR[8:19]
        else:
            self.MAR = self.PC
            self.MBR = self.memory[self.MAR]
            self.IR = self.MBR[:8]
            self.MAR = self.MBR[8:19]
            self.IBR = self.MBR[20:39]

    def execute_instruction(opcode, address):
        if opcode == "00001010":  # LOAD_MQ
            self.AC = self.MQ

        # gotta add the rest too

    def decode(self):
        opcode = self.IR
        address = self.MAR

        self.execute_instruction(opcode, address)

    def execute(self):
        self.fetch()
        self.decode()
