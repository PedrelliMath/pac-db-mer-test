def input_comprehension(input_tuple):
    input_list = [input(f'Digite o {input_name}: ') for input_name in input_tuple]
    return input_list