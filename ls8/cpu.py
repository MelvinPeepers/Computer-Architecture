"""CPU functionality."""

#
# LambdaSchool-8 computer
#


import sys

# found these in the program = []
HLT = 0b00000001  # 1 Step 4 Add the HLT instruction definition
# 130 Step 5 Add the LDI instruction See the LS-8 spec for the details of what this instructions does and its opcode value.
LDI = 0b10000010
PRN = 0b01000111  # 73 Step 6 Add the PRN instruction


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        # Step 1 add list properties to the CPU class to hold 256 bytes of memory
        # and 8 general-purpose registers. Also add properties for any internal
        # registers you need, e.g. PC
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.pc = 0

        # Step 2
        # You don't need to add the MAR or MDR to your CPU class,
        # but they would make handy parameter names for ram_read()
        # and ram_write(), if you wanted.
    def ram_read(self, mar):
        # Step 2 should accept the address to read and return the value stored there.
        # The MAR contains the address that is being read or written to
        return self.ram[mar]

    def ram_write(self, mdr, mar):
        # Step 2 should accept a value to write, and the address to write it to.
        # The MDR contains the data that was read or the data to write.
        self.ram[mar] = mdr

    def load(self):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:

        program = [
            # From print8.ls8
            0b10000010,  # LDI R0,8
            0b00000000,
            0b00001000,
            0b01000111,  # PRN R0
            0b00000000,
            0b00000001,  # HLT
        ]

        for instruction in program:
            self.ram[address] = instruction
            address += 1

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        # elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            # self.fl,
            # self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        # needs to read the memory address that's stored in register PC,
        # and store that result in IR, the Instruction Register. This can
        # just be a local variable in run().

        running = True

        while running:
            ir = self.ram_read(self.pc)  # similiar to command = memory[pc]
            # Using ram_read(), read the bytes at PC+1 and PC+2 from RAM into
            # variables operand_a and operand_b in case the instruction needs them.
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)

            if ir == LDI:
                self.reg[operand_a] = [operand_b]
                self.pc += 3

            elif ir == PRN:
                print(self.reg[operand_a])
                self.pc += 2

            elif ir == HLT:
                running = False
                self.pc += 1

            else:
                # if command is non recognizable
                print("Unknown instruction")
                sys.exit(1)
                # lets crash :(
