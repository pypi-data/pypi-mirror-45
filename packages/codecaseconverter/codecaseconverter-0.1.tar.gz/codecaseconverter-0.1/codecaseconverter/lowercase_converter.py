def convert_camelcase(convert_data):
    for symbol_number in range(len(convert_data)):
        if symbol_number != len(convert_data) - 1:
            if convert_data[symbol_number].islower() and \
                convert_data[symbol_number + 1].isupper():
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
    return convert_data

def _add_delimiter(data, index):
    data = data[:index] + "_" + data[index].lower() + data[index + 1:]
    return data
