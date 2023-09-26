def modulo(multiplicand, base, target):
    multiple = 1
    while True:
        if multiplicand * multiple % base == target:
            break
        multiple += 1

    return multiple
