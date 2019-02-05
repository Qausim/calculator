import re


def evaluate_input(s):
    '''
		Function is useful for evaluating user inputs
		expected to be arithmetical statements and
		evaluates it using taking operators precedence
		into consideration. It returns the answer.
	'''

    # Cancel out all spaces
    s = clear_spaces(s)

    s = populate_operand_open_par_boundary_with_mult_operator(s)

    # Handle all statements that include parentheses
    while '(' in s:
        s = eval_par(s)

    # Get all digits and operators and separate
    num_list = [match[1] for match in re.findall(r'([+-/*(])([-]?\d+)', '+' + s)]

    if s[0] == '-':
        ops_list = re.findall(r'[-+/*]', re.sub(r'([-+/*])(-)|\((-)(\d+)', lambda match: match.group()[0], s[1:]))
    else:
        ops_list = re.findall(r'[-+/*]', re.sub(r'([-+/*])(-)|\((-)(\d+)', lambda match: match.group()[0], s))

    # Perform multiplication operations
    handle_multiplications(num_list, ops_list)

    # Perform division operations
    handle_divisions(num_list, ops_list)

    # Perform addition operations
    handle_additions(num_list, ops_list)

    # Perform substraction operations
    handle_substractions(num_list, ops_list)

    result = float(num_list[0])
    if int(str(result).split('.')[1]) > 0:
        return result
    else:
        return int(result)


def handle_substractions(num_list, ops_list):
    while '-' in ops_list:
        op_index = ops_list.index('-')
        ops_list.pop(op_index)
        rhs = num_list[op_index + 1]
        lhs = num_list[op_index]
        num_list.pop(op_index + 1)
        num_list[op_index] = float(lhs) - float(rhs)


def handle_additions(num_list, ops_list):
    while '+' in ops_list:
        op_index = ops_list.index('+')
        ops_list.pop(op_index)
        rhs = num_list[op_index + 1]
        lhs = num_list[op_index]
        num_list.pop(op_index + 1)
        num_list[op_index] = float(rhs) + float(lhs)


def handle_divisions(num_list, ops_list):
    while '/' in ops_list:
        op_index = ops_list.index('/')
        ops_list.pop(op_index)
        rhs = num_list[op_index + 1]
        lhs = num_list[op_index]
        num_list.pop(op_index + 1)
        num_list[op_index] = float(lhs) / float(rhs)


def handle_multiplications(num_list, ops_list):
    while '*' in ops_list:
        op_index = ops_list.index('*')
        ops_list.pop(op_index)
        rhs = num_list[op_index + 1]
        lhs = num_list[op_index]
        num_list.pop(op_index + 1)
        num_list[op_index] = float(rhs) * float(lhs)


def eval_par(s):
    open_ls = []

    for index in range(len(s)):
        if s[index] == '(':
            open_ls.append(index)
        elif s[index] == ')':
            start = open_ls.pop()
            res = s[:start] + str(evaluate_input(s[(start + 1): index]))
            if len(s[index:]) == 1:
                return res
            else:
                return res + s[index + 1:]

    if '(' in s:
        print('\nError: Uneven parenthesis.\n')
        exit(1)
    return s


def clear_spaces(s):
    return ''.join(re.findall(r'\S', s))


def populate_operand_open_par_boundary_with_mult_operator(s):
    return re.sub(r'\d+\(', lambda match : match.group()[:-1] + '*(', s)


def main():
    while True:
        s = input('Input your statement >>> ')

        print(evaluate_input(s))
        if input('Any more equation to solve? [y/n] >>> ').lower() == 'y':
            continue
        else:
            exit(-1)


main()
