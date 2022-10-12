def Truncate(n, decimals = 0):
    multiplier = 10 ** decimals
    return int(n * multiplier) / multiplier

def DivByZero(variable, replace):
    if variable == 0:
        return replace
    return variable