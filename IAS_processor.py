
class IAS_processor:
    
    def __init__(self, file_name):
        
        self.PC  = 0b0000_0000_0001 # Program counter - 12bits
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
                if x[1][0] == '1':
                    new = ''
                    for char in x[1]:
                        if char=='1':
                            new += '0'
                        else:
                            new += '1'
                    x[1] = int(new, 2) + 1
                else:
                    x[1] = int(x[1], 2)
                self.M[x[0]] = x[1]
        
        for i in range (50):
            self.M[x[0]+1+i] = 0
        
        self.fetch_cycle()
    
    def fetch_cycle(self):
        
        self.MAR = self.PC
        self.MBR = self.M[self.MAR]
        
        self.PC += 1
        
        self.decode_cycle()
    
    def decode_cycle(self):
        
        left_instruction  = self.MBR >> 20 # Gettting the first 20bits for left instruction from MBR
        right_instruction = self.MBR & 0b1111_1111_1111_1111_1111 # Getting the last 20bits for right instruction from MBR
        
        self.IR = left_instruction >> 12 # Getting the first 8bits ie opcode
        self.MAR = left_instruction & 0b1111_1111_1111 # Getting the last 12bits for adress
        self.IBR = right_instruction # Storing right instruction in IBR
        
        self.execute_cycle()
    
    def execute_cycle(self):
    
        # Data transfer instructions
        if self.IR == 0b0000_1010: # LOAD MQ
            self.AC = self.MQ
        
        elif self.IR == 0b0000_1001: # LOAD MQ,M(X)
            self.MBR = self.M[self.MAR]
            self.MQ = self.MBR
        
        elif self.IR == 0b0010_0001: # STOR M(X)
            self.MBR = self.AC
            self.M[self.MAR] = self.MBR
        
        elif self.IR == 0b0000_0001: # LOAD M(X)
            self.MBR = self.M[self.MAR]
            self.AC = self.MBR
        
        elif self.IR == 0b0000_0010: # LOAD -M(X)
            self.MBR = self.M[self.MAR]
            self.MBR = ~self.MBR + 1
            self.AC = self.MBR
        
        elif self.IR == 0b0000_0011: # LOAD |M(X)|
            self.MBR = self.M[self.MAR]
            if self.MBR < 0:
                self.MBR = ~self.MBR + 1
            self.AC = self.MBR
        
        elif self.IR == 0b0000_0100: # LOAD -|M(X)|
            self.MBR = self.M[self.MAR]
            if self.MBR < 0:
                self.MBR = ~self.MBR + 1
            self.MBR = ~self.MBR + 1
            self.AC = self.MBR
        
        # Unconditional branch instructions
        elif self.IR == 0b0000_1101: # JUMP M(X,0:19)
            self.PC = self.MAR
            self.fetch_cycle()
        
        elif self.IR == 0b0000_1110: # JUMP M(X,20:39)
            self.PC = self.MAR
            self.IBR = 0b0000_0000_0000_0000_0000 #resetting IBR
            
            # kind of fetch cycle
            self.MAR = self.PC
            self.MBR = self.M[self.MAR]
            self.PC +=1
            
            # kind of decode cycle with ignoring left instruction
            right_instruction = self.MBR & 0b1111_1111_1111_1111_1111
            self.IR = right_instruction >> 12
            self.MAR = right_instruction & 0b1111_1111_1111
            
            # going to execute cycle
            self.execute_cycle()
        
        # Conditional branch instructions
        elif self.IR == 0b0000_1111: # JUMP+ M(X,0:19)
            if self.AC >= 0:
                self.PC = self.MAR
                self.fetch_cycle()
        
        elif self.IR == 0b0001_0000: # JUMP+ M(X,20:39)
            if self.AC >= 0:
                self.PC = self.MAR
                self.IBR = 0b0000_0000_0000_0000_0000 #resetting IBR
                
                # kind of fetch cycle
                self.MAR = self.PC
                self.MBR = self.M[self.MAR]
                self.PC +=1
                
                # kind of decode cycle with ignoring left instruction
                right_instruction = self.MBR & 0b1111_1111_1111_1111_1111
                self.IR = right_instruction >> 12
                self.MAR = right_instruction & 0b1111_1111_1111
                
                # going to execute cycle
                self.execute_cycle()
        
        # Arithmetic instructions
        elif self.IR == 0b0000_0101: # ADD M(X)
            self.MBR = self.M[self.MAR]
            self.AC = self.AC + self.MBR
        
        elif self.IR == 0b0000_0111: # ADD |M(X)|
            self.MBR = self.M[self.MAR]
            if self.MBR < 0:
                self.MBR = ~self.MBR + 1
            self.AC = self.AC + self.MBR
        
        elif self.IR == 0b0000_0110: # SUB M(X)
            self.MBR = self.M[self.MAR]
            self.AC = self.AC - self.MBR
        
        elif self.IR == 0b0000_1000: # SUB |M(X)|
            self.MBR = self.M[self.MAR]
            if self.MBR < 0:
                self.MBR = ~self.MBR + 1
            self.AC = self.AC - self.MBR
        
        elif self.IR == 0b0000_1011:
            self.MBR = self.M[self.MAR]
            Product = self.MQ * self.MBR
            self.AC = Product >> 40
            self.MQ = Product & 0b1111_1111_1111_1111_1111_1111_1111_1111_1111_1111
        
        elif self.IR == 0b0000_1100: # DIV M(X)
            self.MBR = self.M[self.MAR]
            Quotient = self.AC // self.MBR
            Remainder = self.AC % self.MBR
            self.AC = Remainder
            self.MQ = Quotient
        
        elif self.IR == 0b0001_0100: # LSH
            self.AC = self.AC << 1
        
        elif self.IR == 0b0001_0101: # RSH
            self.AC = self.AC >> 1
        
        # Adress modify instructions
        elif self.IR == 0b0001_0010: # STOR M(X,8:19)
            self.MBR = self.M[self.MAR]
            left_instruction = self.MBR >> 20
            right_instruction = self.MBR & 0b1111_1111_1111_1111_1111
            left_instruction = (left_instruction & 0b0000_0000_0000) | (self.AC & 0b1111_1111_1111)
            self.MBR = (left_instruction << 20) | right_instruction
            self.M[self.MAR] = self.MBR
        
        elif self.IR == 0b0001_0011: # STOR M(X,28:39)
            self.MBR = self.M[self.MAR]
            self.MBR = (self.MBR & 0b0000_0000_0000) | (self.AC & 0b1111_1111_1111)
            self.M[self.MAR] = self.MBR
        
        elif self.IR == 0b0001_1100:
            return
        
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
print(a.AC)