def bit_or_qubit(user_input):
    user_input = user_input.strip().lower()

    if user_input in ['0', '1']:
        return "This is a classical bit."

    try:
        complex_input = complex(user_input)

        if abs(complex_input) ** 2 <= 1:
            return "This is a qubit."
        else:
            return "Invalid qubit state. The squared magnitude should be <= 1."
    except ValueError:
        return "Invalid input. Please enter 0, 1, or a complex number."


if __name__ == '__main__':
    examples = [
    '0',
    '1',
    '0.5+0.5j',
    '1+0j',
    '0.707+0.707j',
    '2+2j',
    'hello'
    ]
    for example in examples:
        result = bit_or_qubit(example)
        print(f"Input: {example}")
        print(f"Result: {result}\n")