DIVIDER = "============================================================"

def get_router_for_network(network):
    if network == 56:
        #return  "0x10ED43C718714eb63d5aA57B78B54704E256024E" #v1
        return   "0x05fF2B0DB69458A0750badebc4f9e13aDd608C7F" #v2
    elif network == 1:
        return  "0x7a250d5630B4cF539739dF2C5dAcb4c659F2488D"

def get_factory_for_network(network):
    if network == 56:
        return   "0xBCfCcbde45cE874adCB698cC183deBcF17952812"
    elif network == 1:
        return  "0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f"

def get_usdt_token_address(network):
    if network == 56:
        return   "0x55d398326f99059ff775485246999027b3197955"
    elif network == 1:
        return  "0xdac17f958d2ee523a2206206994597c13d831ec7"

def to_fixed(number, decimals=0):
    """
    Rounds a number to a fixed number of decimal places.

    Args:
        number (float): The number to be rounded.
        decimals (int): The number of decimal places to round to (default: 0).

    Returns:
        str: The rounded number as a string with the specified decimal places.
    """
    factor = 10 ** decimals
    rounded_number = round(number * factor) / factor
    return format(rounded_number, f".{decimals}f")