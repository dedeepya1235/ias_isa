
class IAS_processor:
    
    def __init__(self, PC, memory_size, file_name):
        
        self.PC  = PC # Program counter - 12 bits
        self.AC  = 0b0000_0000_0000_0000_0000_0000_0000_0000_0000_0000 # Accumulator - 40 bits
        self.IR  = 0b0000_0000 # Instruction register - 8 bits
        self.MAR = 0b0000_0000_0000 # Memory address register - 12 bits
        self.MBR = 0b0000_0000_0000_0000_0000_0000_0000_0000_0000_0000 # Memory buffer register - 40 bits
        self.IBR = 0b0000_0000_0000_0000_0000 # Instruction buffer register - 20 bits
        self.MQ  = 0b0000_0000_0000_0000_0000_0000_0000_0000_0000_0000 # Multiplier/Quotient - 40 bits
        self.M   = {} # Main memory with 12-bit address keys and 40-bit values
        
        # Initialize memory with zeros
        for i in range (memory_size):
            self.M[i+1] = 0
        
        # Loading machine code from file_name into memory
        with open(file_name, 'r') as file:
            lines = file.readlines()
            for line in lines:
                line = line.strip()
                x = line.split(' ')
                x[0] = int(x[0], 2)
                if x[1][0] == '1':
                    # Converting two's compliment machine code to negative numbers
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
        
        # Start executing instructions
        self.processing()
    
    def processing(self):
        # A flag which pushes the IAS machine into the right process - Fetch, Load or Execute
        flag = "fetch"
        
        while True:
            # Executing Fetch cycle
            if flag == "fetch":
                # if IBR is empty Address for the instruction is being fetched from PC to MAR which
                # loads that memory location into MBR and PC is incremented by one
                if not self.IBR:
                    self.MAR = self.PC
                    self.MBR = self.M[self.MAR]
                    
                    self.PC += 1
                    
                    flag = "load"
                # else the right instruction stored in IBR is loaded
                else:
                    self.IR = self.IBR >> 12 # Getting the first 8bits ie opcode
                    self.MAR = self.IBR & 0b1111_1111_1111 # Getting the last 12bits for adress
                    
                    self.IBR = 0b0000_0000_0000_0000_0000 # resetting IBR after it's use
                    
                    flag = "execute"
            
            # Loads the instructions into Program control unit
            if flag == "load":
                # Separating left and the right instruction from MBR
                left_instruction  = self.MBR >> 20 # First 20-bits of MBR
                right_instruction = self.MBR & 0b1111_1111_1111_1111_1111 # Last 20-bits of MBR
                
                # Extracting opcode and address from left instruction
                self.IR = left_instruction >> 12 # First 8-bits of left instruction
                self.MAR = left_instruction & 0b1111_1111_1111 # Last 12-bits of left instruction
                
                # Storing right instruction in IBR
                self.IBR = right_instruction
                
                flag = "execute"
            
            # Executing Execute cycle
            # Decodes the instruction from the opcode and
            # Acts like an ALU which performs the required operation based on the opcode
            if flag == "execute":
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
                    self.IBR = 0b0000_0000_0000_0000_0000 #resetting IBR
                    flag = "fetch"
                    continue
                
                elif self.IR == 0b0000_1110: # JUMP M(X,20:39)
                    self.PC = self.MAR
                    
                    # Similar to fetch cycle
                    self.MAR = self.PC
                    self.MBR = self.M[self.MAR]
                    self.PC += 1
                    
                    # Loading only the right instruction into IBR
                    self.IBR = self.MBR & 0b1111_1111_1111_1111_1111
                    
                    # going to fetch cycle
                    flag = "fecth"
                    continue
                
                # Conditional branch instructions
                elif self.IR == 0b0000_1111: # JUMP+ M(X,0:19)
                    if self.AC >= 0:
                        self.PC = self.MAR
                        self.IBR = 0b0000_0000_0000_0000_0000 # resetting IBR
                        flag = "fetch"
                        continue
                
                elif self.IR == 0b0001_0000: # JUMP+ M(X,20:39)
                    if self.AC >= 0:
                        self.PC = self.MAR
                        
                        # Similar to fetch cycle
                        self.MAR = self.PC
                        self.MBR = self.M[self.MAR]
                        self.PC += 1
                        
                        # Loading only the right instruction in IBR
                        self.IBR = self.MBR & 0b1111_1111_1111_1111_1111
                        
                        # going to execute cycle
                        flag == "fetch"
                        continue
                
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
                
                elif self.IR == 0b0000_1011: # MUL M(X)
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
                    left_instruction = (left_instruction & 0b1111_1111_0000_0000_0000) | (self.AC & 0b1111_1111_1111)
                    self.MBR = (left_instruction << 20) | right_instruction
                    self.M[self.MAR] = self.MBR
                
                elif self.IR == 0b0001_0011: # STOR M(X,28:39)
                    self.MBR = self.M[self.MAR]
                    self.MBR = (self.MBR & 0b1111_1111_1111_1111_1111_1111_1111_0000_0000_0000) | (self.AC & 0b1111_1111_1111)
                    self.M[self.MAR] = self.MBR
                
                elif self.IR == 0b0001_1100: # NOP
                    break
                
                # Extra instructions added by us
                elif self.IR == 0b0010_0000: # INCR AC
                    self.AC += 1
                
                elif self.IR == 0b0010_0010: # DECR AC
                    self.AC -= 1
                
                # heading back to fetch cycle
                flag = "fetch"
a = IAS_processor(20, 50, "machine_code.txt")
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