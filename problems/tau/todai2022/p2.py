
def seq(n):
    x = 1
    for i in range(1, n):
        x = x * x + 1
    return x

def check_a3n_is_a_multiple_of_5(n):
    for i in range(3, n, 3):
        assert(seq(i) % 5 == 0)
    print("OK")
        
