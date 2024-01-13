
class IAS_processor:
    
    def __init__(self, file_name):
        
        self.PC  = 0b0000_0000_0000 # Program counter - 12bits
        self.AC  = 0b0000_0000_0000_0000_0000_0000_0000_0000_0000_0000 # Accumulator - 40bits
        self.IR  = 0b0000_0000 # Instruction register - 8bits
        self.MAR = 0b0000_0000_0000 # Memory address register - 12bits
        self.MBR = 0b0000_0000_0000_0000_0000_0000_0000_0000_0000_0000 # Memory buffer register - 40bits
        self.IBR = 0b0000_0000_0000_0000_0000 # Instruction buffer register - 20bits
        self.MQ  = 0b0000_0000_0000_0000_0000_0000_0000_0000_0000_0000 # Multiplier/Quotient - 40bits
        self.M   = {} # Main memory with 12bit address keys and 40bit values
        
        with open(file_name, 'r') as file:
            lines = file.readlines()
            for line in lines:
                line = line.strip()
                x = line.split(' ')
                x[0] = int(x[0], 2)
                x[1] = int(x[1], 2)
                self.M[x[0]] = x[1]
        
        self.fetch_cycle()
    
    def fetch_cycle(self):
        
        self.MAR = self.PC
        self.MBR = self.M[self.MAR]
        
        self.pc += 1
        
        self.decode_cycle()
    
    def decode_cycle(self):
        
        left_instruction  = self.MBR >> 20 # Gettting the first 20bits for left instruction from MBR
        right_instruction = self.MBR & 0b1111_1111_1111_1111_1111 # Getting the last 20bits for right instruction from MBR
        
        self.IR = left_instruction >> 12 # Getting the first 8bits ie opcode
        self.MAR = left_instruction & 0b1111_1111_1111 # Getting the last 12bits for adress
        self.IBR = right_instruction # Storing right instruction in IBR
        
        self.MBR = 0b0000_0000_0000_0000_0000_0000_0000_0000_0000_0000 # resetting MBR after it's use
        
        self.execute_cycle()
    
    def execute_cycle(self):
    
        # Data transfer instructions
        if self.IR == 0b0000_1010:
            pass # implement LOAD MQ
        
        elif self.IR == 0b0000_1001:
            pass # implement LOAD MQ,M(X)
        
        elif self.IR == 0b0010_0001:
            pass # implement STOR M(X)
        
        elif self.IR == 0b0000_0001:
            pass # implement LOAD M(X)
        
        elif self.IR == 0b0000_0010:
            pass # implement LOAD -M(X)
        
        elif self.IR == 0b0000_0011:
            pass # implement LOAD |M(X)|
        
        elif self.IR == 0b0000_0100:
            pass # implement LOAD -|M(X)|
        
        # Unconditional branch instructions
        elif self.IR == 0b0000_1101:
            pass # implement JUMP M(X,0:19)
        
        elif self.IR == 0b0000_1110:
            pass # implement JUMP M(X,20:39)
        
        # Conditional branch instructions
        elif self.IR == 0b0000_1111:
            pass # implement JUMP+ M(X,0:19)
        
        elif self.IR == 0b0001_0000:
            pass # implement JUMP+ M(X,20:39)
        
        # Arithmetic instructions
        elif self.IR == 0b0000_0101:
            pass # implement ADD M(X)
        
        elif self.IR == 0b0000_0111:
            pass # implement ADD |M(X)|
        
        elif self.IR == 0b0000_0110:
            pass # implement SUB M(X)
        
        elif self.IR == 0b0000_1000:
            pass # implement SUB |M(X)|
        
        elif self.IR == 0b0000_1011:
            pass # implement MUL M(X)
        
        elif self.IR == 0b0000_1100:
            pass # implement DIV M(X)
        
        elif self.IR == 0b0001_0100:
            pass # implement LSH
        
        elif self.IR == 0b0001_0101:
            pass # implement RSH
        
        # Adress modify instructions
        elif self.IR == 0b0001_0010:
            pass # implement STOR M(X,8:19)
        
        elif self.IR == 0b0001_0011:
            pass # implement STOR M(X,28:39)
        
        self.IR = 0b0000_0000 # resetting IR after use
        self.MAR = 0b0000_0000_0000 # resetting MAR after use
        
        if self.IBR:
            self.IR = self.IBR >> 12 # Getting the first 8bits ie opcode
            self.MAR = self.IBR & 0b1111_1111_1111 # Getting the last 12bits for adress
            
            self.IBR = 0b0000_0000_0000_0000_0000 # resetting IBR after it's use
            
            self.execute_cycle()
        
        else:
            self.fetch_cycle()

a = IAS_processor("machine_code.txt")