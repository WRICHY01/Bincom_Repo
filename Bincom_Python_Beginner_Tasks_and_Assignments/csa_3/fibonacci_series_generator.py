def generate_fibonacci_series(n):
    a = 0
    prev = 0
    current = 0
    fib_ser = []

    for i in range(n):
        fib_ser.append(a)
        a = prev + current
        prev = current
        if a < 1:
            a += 1

        current = a

        


    return fib_ser



print(generate_fibonacci_series(5))