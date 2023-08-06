def convert_lowercase(convert_data):
    symbol_number = 0
    while symbol_number < len(convert_data) - 1:
        if (convert_data[symbol_number] == "_" and
                convert_data[symbol_number + 1].isalpha() and
                convert_data[symbol_number - 1].isalpha()):
            convert_data = _remove_delimiter(
                convert_data,
                symbol_number
            )
        symbol_number += 1
    return convert_data

def _remove_delimiter(data, index):
    convert_data = data[:index] + data[index + 1].upper()
    if index + 2 < len(data):
        convert_data += data[index + 2:]
    return convert_data
