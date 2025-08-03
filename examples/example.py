from ngpasm.program import ASMProgram, ProgramMode
from ngpasm.mnemonics.arithmetic import AddMnemonic

prog = ASMProgram("test.asm", ProgramMode.x64bit)
regs = prog.regs

prog.insert_mnemonic(AddMnemonic(regs.AX, regs.BX))
prog.insert_mnemonic(AddMnemonic(regs.CX, regs.BX))
prog.insert_mnemonic(AddMnemonic(regs.DX, regs.BX))
print(prog.generate())
