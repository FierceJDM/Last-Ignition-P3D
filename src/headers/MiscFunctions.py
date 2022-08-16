def Truncate(n, decimals = 0):
    multiplier = 10 ** decimals
    return int(n * multiplier) / multiplier

def TranslatePercentage(percent, total, variable):
    if percent > 100:
        percent = 100
    elif percent < -100:
        percent = -100
    if percent < 0:
        if variable > -total:
            variable += total*percent/100
    else:
        if variable < total:
            variable += total*percent/100
    return variable