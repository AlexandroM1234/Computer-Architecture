"""CPU functionality."""
import sys
HLT = 0b00000001
LDI = 0b10000010
PRN  = 0b01000111
MUL = 0b10100010
POP = 0b01000110
PUSH  = 0b01000101
ADD = 0b10100000
CALL = 0b01010000 
RET = 0b00010001
CMP = 0b10100111
JMP = 0b01010100
JEQ = 0b01010101
JNE = 0b01010110
class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0]*256
        self.reg = [0]*8
        self.pc = 0
        self.running = False
        self.sp = 7
        self.flags = 0b00000000
        self.branchtable = {
            HLT : self.hlt_func,
            LDI : self.ldi_func,
            PRN : self.prn_func,
            MUL : self.mult_func,
            POP : self.pop_func,
            PUSH : self.push_func,
            ADD : self.add_func,
            CALL : self.call_func,
            RET : self.ret_func,
            CMP : self.CMP, 
            JMP : self.jump_func,
            JEQ : self.jeq_func,
            JNE : self.jne_func
        }

    def ram_read(self,address):
        return self.ram[address]

    def ram_write(self,value,address):
        self.ram[address] = value
        # self.ram[address]

    file = sys.argv[1]
    def load(self,file):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:

        # program = [
        #     # From print8.ls8
        #     0b10000010, # LDI R0,8
        #     0b00000000,
        #     0b00001000,
        #     0b01000111, # PRN R0
        #     0b00000000,
        #     0b00000001, # HLT
        # ]
        try:
            # print(sys.argv[1])
            with open(file) as f:
                for line in f:
                    line  = line.split("#")[0].strip()

                    if line == '':
                        continue

                    self.ram[address] = int(line,2)
                    address +=1

        except:
            print("can not find it!")

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""
        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
        elif op == "CMP":
            if self.reg[reg_a] < self.reg[reg_b]:
                self.flags = 0b00000100

            elif self.reg[reg_a] > self.reg[reg_b]:
                self.flags =  0b00000010

            elif self.reg[reg_a] == self.reg[reg_b]:
                self.flags =  0b00000001
            else:
                self.flags = 0b00000000
        else:
            raise Exception("Unsupported ALU operation")
        
    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

    def CMP (self):
        reg_a = self.ram_read(self.pc+1)
        reg_b = self.ram_read(self.pc+2)
        self.alu("CMP",reg_a,reg_b)
        self.pc += 3
    
    def jump_func(self):
        reg_address = self.ram_read(self.pc + 1)
        self.pc = self.reg[reg_address]

    def jeq_func(self):
        if self.flags == 1:
            # use jump method to get to the address stored in the given register
            self.jump_func()
        else:
            self.pc +=2

    def jne_func(self):
        if self.flags != 1:
            # use jump method to get to th address stored in the given register
            self.jump_func()
        else:
            self.pc += 2
            
    def prn_func(self):
        register_address = self.ram_read(self.pc+1)
        print(self.reg[register_address])
        self.pc += 2
    
    def ldi_func(self):
        register_address  =self.ram_read(self.pc+1)
        value = self.ram_read(self.pc+2)
        self.reg[register_address] = value
        self.pc += 3

    def add_func(self):
        regA = self.ram_read(self.pc+1)
        regB = self.ram_read(self.pc+2)
        self.alu("ADD",regA,regB)
        self.pc +=3
        
    def mult_func(self):
        regA = self.ram_read(self.pc+1)
        regB = self.ram_read(self.pc+2)
        self.alu("MUL",regA,regB)
        self.pc +=3

    def pop_func(self):
        value = self.ram_read(self.reg[self.sp])
        reg_address = self.ram_read(self.pc+1)
        self.reg[reg_address] = value
        self.reg[self.sp] += 1 
        self.pc +=2

    def push_func(self):
        self.reg[self.sp] -= 1
        reg_address = self.ram_read(self.pc+1)
        memory_adress = self.reg[self.sp]
        value = self.reg[reg_address]
        self.ram_write(value,memory_adress)
        self.pc +=2

    def call_func(self):
        # self.reg[self.sp] -= 1
        # self.ram[self.reg[self.sp]] = self.pc + 2

        # reg = self.ram[self.pc + 1]
        # self.pc = self.reg[reg]
        ret = self.pc + 2
        self.reg[self.sp] -= 1

        self.ram_write(ret,self.reg[self.sp]) 
        self.pc = self.reg[self.ram_read(self.pc + 1)]

    def ret_func(self):
        # self.pc = self.ram[self.reg[self.sp]]
        # self.reg[self.sp] += 1
        value=self.ram_read(self.reg[self.sp])
        self.pc = value
        self.reg[self.sp] += 1

    def hlt_func (self):
        self.running = False

    def run(self):
        """Run the CPU."""

        self.reg[self.sp] = 0xF4
        self.running = True       
        while self.running:
            IR = self.ram_read(self.pc)
            self.branchtable[IR]()
