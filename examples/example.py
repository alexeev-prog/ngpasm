from ngpasm.mnemonics.arithmetic import AddMnemonic
from ngpasm.program import ASMProgram, ProgramMode
from ngpasm.registers import BaseRegisterSet

prog = ASMProgram("test.asm", ProgramMode.BIT_64)
regs: BaseRegisterSet | None = prog.registers

prog.add_mnemonic(AddMnemonic(regs.AX, regs.BX))
prog.add_mnemonic(AddMnemonic(regs.CX, regs.BX))
prog.add_mnemonic(AddMnemonic(regs.DX, regs.BX))
print(prog.generate())
