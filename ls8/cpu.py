"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0]*256
        self.reg = [0]*8
        self.pc = 0

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
        if op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
        #elif op == "SUB": etc
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

        print()

    def run(self):
        """Run the CPU."""
        running = True
        while running:
            IR = self.ram_read(self.pc)
            if IR  == 0b00000001:
                running = False
            elif IR == 0b10000010:
                register_address  =self.ram_read(self.pc+1)
                value = self.ram_read(self.pc+2)
                self.reg[register_address] = value
                self.pc += 3
            elif IR == 0b01000111:
                register_address = self.ram_read(self.pc+1)
                print(self.reg[register_address])
                self.pc += 2
            elif IR == 0b10100010:
                regA = self.ram_read(self.pc+1)
                regB = self.ram_read(self.pc+2)
                self.alu("MUL",regA,regB)
                self.pc +=3