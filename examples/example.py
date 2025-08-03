from ngpasm.mnemonics.arithmetic import AddMnemonic
from ngpasm.program import ASMProgram, ProgramMode

prog = ASMProgram("test.asm", ProgramMode.x64bit)
regs = prog.regs

prog.insert_mnemonic(AddMnemonic(regs.AX, regs.BX))
prog.insert_mnemonic(AddMnemonic(regs.CX, regs.BX))
prog.insert_mnemonic(AddMnemonic(regs.DX, regs.BX))
print(prog.generate())
