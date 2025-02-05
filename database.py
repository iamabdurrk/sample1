def even_or_odd(n):
    return "Even" if n % 2 == 0 else "Odd"

num = int(input("Enter a number: "))
print(f"{num} is {even_or_odd(num)}.")
