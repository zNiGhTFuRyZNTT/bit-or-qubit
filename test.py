import cmath
import random
from main import bit_or_qubit

# Metamorphic Relations
def MR1_conjugate(input_str):
    # Conjugate of a qubit should still be a valid qubit
    try:
        z = complex(input_str)
        conjugate = complex(z.real, -z.imag)
        return bit_or_qubit(str(z)) == bit_or_qubit(str(conjugate))
    except ValueError:
        return True  # Non-complex inputs are not affected by this relation

def MR2_scale(input_str):
    # Scaling a qubit by a factor < 1 should still be a valid qubit
    try:
        z = complex(input_str)
        scaled = z * 0.5
        return (bit_or_qubit(str(z)) == "This is a qubit") == (bit_or_qubit(str(scaled)) == "This is a qubit")
    except ValueError:
        return True  # Non-complex inputs are not affected by this relation

# Generate test cases
def generate_test_cases(n=100):
    test_cases = []
    
    for _ in range(n):
        
        case_type = random.choice(['bit', 'valid_qubit', 'invalid_qubit', 'invalid_input'])
        
        if case_type == 'bit':
            test_cases.append(random.choice(['0', '1']))
            
        elif case_type == 'valid_qubit':
            r = random.uniform(0, 1)
            theta = random.uniform(0, 2*cmath.pi)
            z = cmath.rect(r, theta)
            test_cases.append(f"{z.real}+{z.imag}j")
            
        elif case_type == 'invalid_qubit':
            r = random.uniform(1.01, 2)
            theta = random.uniform(0, 2*cmath.pi)
            z = cmath.rect(r, theta)
            test_cases.append(f"{z.real}+{z.imag}j")
            
        else:
            test_cases.append('invalid_input')
    return test_cases

# Run metamorphic tests
def run_metamorphic_tests(test_cases):
    
    mr1_results = [MR1_conjugate(case) for case in test_cases]
    mr2_results = [MR2_scale(case) for case in test_cases]
    
    return mr1_results, mr2_results

# Mutation testing
def generate_mutants():
    mutants = []
    
    # Mutant 1: Change <= to <
    def mutant1(user_input):
        user_input = user_input.strip().lower()
        if user_input in ['0', '1']:
            return "This is a classical bit."
        try:
            complex_input = complex(user_input)
            if abs(complex_input) ** 2 < 1:  # Changed <= to <
                return "This is a qubit."
            else:
                return "Invalid qubit state. The squared magnitude should be < 1."
        except ValueError:
            return "Invalid input. Please enter 0, 1, or a complex number."
    
    # Mutant 2: Change squared magnitude calculation
    def mutant2(user_input):
        user_input = user_input.strip().lower()
        if user_input in ['0', '1']:
            return "This is a classical bit."
        try:
            complex_input = complex(user_input)
            if abs(complex_input) <= 1:  # Removed squaring
                return "This is a qubit."
            else:
                return "Invalid qubit state. The magnitude should be <= 1."
        except ValueError:
            return "Invalid input. Please enter 0, 1, or a complex number."
    
    mutants.append(mutant1)
    mutants.append(mutant2)
    return mutants

# Run mutation testing
def run_mutation_testing(test_cases, mutants):
    original_results = [bit_or_qubit(case) for case in test_cases]
    killed_mutants = [0] * len(mutants)
    
    for i, mutant in enumerate(mutants):
        mutant_results = [mutant(case) for case in test_cases]
        if mutant_results != original_results:
            killed_mutants[i] = 1
    
    return killed_mutants

# Main execution
if __name__ == "__main__":
    test_cases = generate_test_cases()
    
    print("Running Metamorphic Tests:")
    mr1_results, mr2_results = run_metamorphic_tests(test_cases)
    print(f"MR1 (Conjugate) passed: {sum(mr1_results)}/{len(mr1_results)}")
    print(f"MR2 (Scale) passed: {sum(mr2_results)}/{len(mr2_results)}")
    
    print("\nRunning Mutation Testing:")
    mutants = generate_mutants()
    killed_mutants = run_mutation_testing(test_cases, mutants)
    print(f"Mutants killed: {sum(killed_mutants)}/{len(mutants)}")

# Run example inputs
examples = ['0', '1', '0.5+0.5j', '1+0j', '0.707+0.707j', '2+2j', 'hello']
print("\nExample Inputs:")
for example in examples:
    result = bit_or_qubit(example)
    print(f"Input: {example}")
    print(f"Result: {result}\n")