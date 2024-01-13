
class IAS_processor:
    
    def __init__(self):
        self.PC  = 0b000000000000 # Program counter - 12bits
        self.AC  = 0b0000000000000000000000000000000000000000 # Accumulator - 40bits
        self.IR  = 0b00000000 # Instruction register - 8bits
        self.MAR = 0b000000000000 # Memory address register - 12bits
        self.MBR = 0b0000000000000000000000000000000000000000 # Memory buffer register - 40bits
        self.IBR = 0b00000000000000000000 # Instruction buffer register - 20bits
        self.MQ  = 0b0000000000000000000000000000000000000000 # Multiplier/Quotient - 40bits
        self.M   = {} # Main memory with 12bit address keys and 40bit values
    
    def fetch_cycle(self):
        self.MAR = self.PC
        self.MBR = self.M[self.MAR]
        left_instruction  = self.MBR >> 20
        right_instruction = self.MBR & 0b11111111111111111111
        self.IR = left_instruction >> 12
        self.MAR = left_instruction & 0b111111111111
        self.IBR = right_instruction
        self.pc += 1
    
    def decode_cycle(self):
        