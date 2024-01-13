
class IAS_processor:
    
    def __init__(self):
        
        self.PC  = 0b0000_0000_0000 # Program counter - 12bits
        self.AC  = 0b0000_0000_0000_0000_0000_0000_0000_0000_0000_0000 # Accumulator - 40bits
        self.IR  = 0b0000_0000 # Instruction register - 8bits
        self.MAR = 0b0000_0000_0000 # Memory address register - 12bits
        self.MBR = 0b0000_0000_0000_0000_0000_0000_0000_0000_0000_0000 # Memory buffer register - 40bits
        self.IBR = 0b0000_0000_0000_0000_0000 # Instruction buffer register - 20bits
        self.MQ  = 0b0000_0000_0000_0000_0000_0000_0000_0000_0000_0000 # Multiplier/Quotient - 40bits
        self.M   = {} # Main memory with 12bit address keys and 40bit values
    
    def fetch_cycle(self):
        
        self.MAR = self.PC
        self.MBR = self.M[self.MAR]
        
        self.pc += 1
    
    def decode_cycle(self):
        
        left_instruction  = self.MBR >> 20 # Gettting the first 20bits for left instruction from MBR
        right_instruction = self.MBR & 0b1111_1111_1111_1111_1111 # Getting the last 20bits for right instruction from MBR
        
        self.IR = left_instruction >> 12 # Getting the first 8bits ie opcode
        self.MAR = left_instruction & 0b1111_1111_1111 # Getting the last 12bits for adress
        self.IBR = right_instruction # Storing right instruction in IBR
        
        self.MBR = 0b0000_0000_0000_0000_0000_0000_0000_0000_0000_0000 # resetting MBR after it's use
    
    def execute_cycle(self):
        
        if self.IR == 0b0000_1010:
            pass # implement LOAD MQ
        elif self.IR == 0b0000_1001:
            pass # implement LOAD MQ,M(X)
        elif self.IR == 0b0010_0001:
            pass # implement STOR M(X)
        elif self.IR == 0b0000_0001:
            pass # implement LOAD M(X)