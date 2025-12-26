



magic_table = {20: {5: 51, 6: 47, 8: 39, 10: 32, 12: 27, 15: 21, 18: 17, 20: 15},
    18: {5: 43, 6: 39, 8: 33, 10: 28, 12: 23, 15: 19, 18: 15, 20: 13},
    15: {5: 34, 6: 31, 8: 26, 10: 22, 12: 19, 15: 15, 18: 12, 20: 11},
    12: {5: 26, 6: 24, 8: 20, 10: 17, 12: 15, 15: 12, 18: 10, 20: 9},
    10: {5: 22, 6: 20, 8: 17, 10: 15, 12: 13, 15: 11, 18: 9, 20: 8},
    8:  {5: 19, 6: 17, 8: 15, 10: 13, 12: 11, 15: 9, 18: 8, 20: 7},
    6:  {5: 16, 6: 15, 8: 13, 10: 11, 12: 10, 15: 8, 18: 7, 20: 6},
    5:  {5: 15, 6: 14, 8: 12, 10: 11, 12: 9, 15: 8, 18: 7, 20: 6},
    0:  {5: 10, 6: 10, 8: 9, 10: 8, 12: 7, 15: 6, 18: 5, 20: 5}}


def lookup_pe(growth, required_return):
    if growth not in magic_table:
        return None
    if required_return not in magic_table[growth]:
        return None
    return magic_table[growth][required_return]

def value_stock(eps, growth, required_return, margin_of_safety=0.30):
    pe = lookup_pe(growth, required_return)
    if pe is None:
        return None

    intrinsic_value = eps * pe
    buy_price = intrinsic_value * (1 - margin_of_safety)
    return pe, intrinsic_value, buy_price

def valuation_interval(eps, growth, required_return, margin_of_safety=0.30, step = 2):
    scenarios = {}

    for g in [growth - step, growth, growth + step]:
        pe = lookup_pe(g, required_return)
        
        if pe is None:
            continue
    
        intrinsic_value = eps * pe
        buy_price = intrinsic_value * (1 - margin_of_safety)
        
        scenarios[g] = {
            'pe': pe,
            'intrinsic_value': intrinsic_value,
            'buy_price': buy_price
        }   
    return scenarios

