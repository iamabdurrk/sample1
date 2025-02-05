def fibonacci(n):
    if n <= 0:
        return "Input must be a positive integer."
    elif n == 1:
        return [0]
    elif n == 2:
        return [0, 1]
    
    sequence = fibonacci(n - 1)
    sequence.append(sequence[-1] + sequence[-2])
    return sequence

n_terms = int(input("Enter the number of terms: "))
print(fibonacci(n_terms))
