"""
@BY: Yang LIU
@DATE: 15-11-2020
"""


# Input: A string Text.
# Output: SuffixArray(Text).
def inverse_burrows_wheeler_transform(text):
    
    set0 = set(text)
    dic = {}  
    for value in set0:
        value_array = [i for i in text if i == value]
        old_text = [value+str(i) for i in range(1, len(value_array)+1)]
        dic[value] = old_text
    # print(dic)
    symbols = [i for i in set0]
    symbols.sort()
    # print(symbols)
    first_column = []
    for symbol in symbols:
        first_column.extend(dic[symbol])
    # print(first_column)

    last_column = []
    for symbol in text:
        last_column.append(dic[symbol][0])
        dic[symbol].pop(0)


    find_next_symbol = {}
    for i in range(len(last_column)):
        find_next_symbol[last_column[i]] = first_column[i]
    output = []
    symbol = last_column[0]
    first_symbol = symbol

    while symbol in find_next_symbol.keys():
        output.append(find_next_symbol[symbol])
        symbol = find_next_symbol[symbol]
        if symbol == first_symbol:
            break
    result = [i[0] for i in output]
    result = result[1:]
    result.append("$")
    letters = ""
    for value in result:
        letters += value
    return letters

if __name__ == "__main__":   

    text = "enwvpeoseu$llt"
    print(inverse_burrows_wheeler_transform(text))