def convert_camelcase(convert_data):
    symbol_number = 0
    while symbol_number < len(convert_data):
        if symbol_number != len(convert_data) - 1:
            if (convert_data[symbol_number].islower() and
                    convert_data[symbol_number + 1].isupper()):
                convert_data = _add_delimiter(
                    convert_data,
                    symbol_number + 1
                )
        else:
            if convert_data[symbol_number].isupper():
                convert_data = _add_delimiter(
                    convert_data,
                    symbol_number
                )
        symbol_number += 1
    return convert_data

def _add_delimiter(data, index):
    data = data[:index] + "_" + data[index].lower() + data[index + 1:]
    return data
