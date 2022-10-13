def triangle(a):
    a += 1
    spaces = a
    stars = 0
    for k in range(a):
        for i in range(spaces):
            print(" ", end = "")
        for i in range(stars):
            print("*", end = "")
        print("*", end = "")
        for i in range(stars):
            print("*", end = "")
        for i in range(spaces):
            print(" ", end = "")
        spaces -= 1
        stars += 1
        print("")


triangle(5)