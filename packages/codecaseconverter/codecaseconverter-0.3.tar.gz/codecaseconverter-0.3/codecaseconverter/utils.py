def check_exception_word(
        convert_data,
        exception_words,
        exception_words_delimiters,
        word_symbol_number):
    current_symbol_number = word_symbol_number
    if (((word_symbol_number > 0 and
            convert_data[word_symbol_number - 1] in
            exception_words_delimiters) or
            word_symbol_number == 0)):
        word = ""
        while convert_data[word_symbol_number] not in \
                exception_words_delimiters:
            word += convert_data[word_symbol_number]
            word_symbol_number += 1
            if word_symbol_number == len(convert_data):
                break
        if word in exception_words:
            return word_symbol_number
    return current_symbol_number
