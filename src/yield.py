def num_print():
    print("yield—1")
    yield 'yield-1 return'
    print("yield—2")
    yield 'yield-2 return'
    print("yield—3")
    yield 'yield-3 return'
for i in num_print():
    print('i:',i)