from definitions import IMP

def instr_mod(s):
    if s[:2] in IMP.keys():
        return(IMP[s[:2]])
    elif s[0] in IMP.keys():
        return IMP[s[0]]
    else:
        return "INVALID_IMP_INSTRUCTION_MODIFICATION_PARAMETER"