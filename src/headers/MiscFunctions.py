def Truncate(n, decimals = 0):
    multiplier = 10 ** decimals
    return int(n * multiplier) / multiplier

def DivByZero(variable, replace): # Avoid Division by Zero
    if variable == 0:
        return replace
    return variable

def Dampen(currentpos, camoffset, limitpos=0): # Dampen Camera when approaching limit pos
    if limitpos-0.5 < camoffset < limitpos+0.5:
        return currentpos/8
    if limitpos-1.5 < camoffset < limitpos+1.5:
        return currentpos/4
    if limitpos-2.5 < camoffset < limitpos+2.5:
        return currentpos/2
    
    return currentpos
    