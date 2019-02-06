import re


def evaluate_input(s):
    '''
		Function is useful for evaluating user inputs
		expected to be arithmetical statements and
		evaluates it using taking operators precedence
		into consideration. It returns the answer.
	'''
    # If statement contains a letter or '=' raise ValueError
    if len(re.findall(r'[a-zA-z=]', s)) > 0:
        raise ValueError

    # Cancel out all spaces
    s = clear_spaces(s)
    # Populate all digit-open parentheses boundary with no specified operator with the multiply sign
    s = populate_operand_open_par_boundary_with_mult_operator(s)

    # Exit if uneven parentheses
    if len(re.findall(r'\(', s)) != len(re.findall(r'\)', s)):
        raise ArithmeticError("Error: Uneven parentheses.")

    # Make all floating point numbers written in the form '.22' to be in the form '0.22'
    # i.e. populate with a preceding zero
    s = re.sub(r'(\D\.\d+)', lambda match: match.group()[0] + '0' + match.group()[1:], s)

    # Handle all parentheses
    while '(' in s:
        s = eval_par(s)


    # Get all digits and save in a list
    num_list = [match[1] for match in re.findall(r'([+-/*(])(([-]?\d+)(\.)?(\d+)*)', '+' + s)]

    # Get all operators (operates two operands) and save in a list
    if s[0] == '-': # If the first number is negative do not include its negative sign
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
    handle_subtractions(num_list, ops_list)

    result = float(num_list[0])

    # Return int if result is a whole number else return float (at most 10 decimal places)
    if int(str(result).split('.')[1]) > 0:
        return float("%.10f" % result)
    else:
        return int(result)


def handle_subtractions(num_list, ops_list):
    '''
    Handles all subtraction operations
    :param num_list:
    :param ops_list:
    :return: the result of the subtraction operations
    '''
    while '-' in ops_list:
        op_index = ops_list.index('-')
        ops_list.pop(op_index)
        rhs = num_list[op_index + 1]
        lhs = num_list[op_index]
        num_list.pop(op_index + 1)
        num_list[op_index] = float(lhs) - float(rhs)


def handle_additions(num_list, ops_list):
    '''
    Handles all addition operations
    :param num_list:
    :param ops_list:
    :return: the result of the addition operations
    '''
    while '+' in ops_list:
        op_index = ops_list.index('+')
        ops_list.pop(op_index)
        rhs = num_list[op_index + 1]
        lhs = num_list[op_index]
        num_list.pop(op_index + 1)
        num_list[op_index] = float(rhs) + float(lhs)


def handle_divisions(num_list, ops_list):
    '''
    Handles all division operations
    :param num_list:
    :param ops_list:
    :return: the result of the division operations
    '''
    while '/' in ops_list:
        op_index = ops_list.index('/')
        ops_list.pop(op_index)
        rhs = num_list[op_index + 1]
        lhs = num_list[op_index]
        num_list.pop(op_index + 1)
        num_list[op_index] = float(lhs) / float(rhs)


def handle_multiplications(num_list, ops_list):
    '''
    Handles all multiplication operations
    :param num_list:
    :param ops_list:
    :return: the result of the multiplication operation
    '''
    while '*' in ops_list:
        op_index = ops_list.index('*')
        ops_list.pop(op_index)
        rhs = num_list[op_index + 1]
        lhs = num_list[op_index]
        num_list.pop(op_index + 1)
        num_list[op_index] = float(rhs) * float(lhs)


def eval_par(s):
    '''
    Handles parentheses that occur in statement
    :param s:
    :return: the result after each parentheses handling
    '''
    open_ls = [] # A to contain the indices of the open parentheses encountered
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
        raise ArithmeticError("Error: Bad/Uneven parentheses combination.")
    return s


def clear_spaces(s):
    '''
    Clears all spaces that occur in the statement
    :param s:
    :return:
    '''
    return ''.join(re.findall(r'\S', s))


def populate_operand_open_par_boundary_with_mult_operator(s):
    '''
    Manipulate all digit-open parentheses boundaries without operator with multiplication operator
    :param s:
    :return:
    '''
    return re.sub(r'\d+\(', lambda match : match.group()[:-1] + '*(', s)


def main():
    while True:
        s = input('Input your statement >>> ')

        try:
            print(evaluate_input(s))
            if input('Any more equation to solve? [y/n] >>> ').lower() == 'y':
                continue
            else:
                exit(0)
        except (ValueError, ArithmeticError, TypeError, IndexError) as e:
            generic_error_msg = "Error: Bad statement."
            switcher = {ValueError: e.args[0] if len(e.args) > 0 else generic_error_msg,
                        ArithmeticError: e.args[0] if len(e.args) > 0 else generic_error_msg,
                        TypeError: generic_error_msg,
                        IndexError: generic_error_msg
                        }
            print(switcher[type(e)])
            exit(1)


main()
