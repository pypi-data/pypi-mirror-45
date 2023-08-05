def max_olokh(*toonuud):
    max = toonuud[0]
    for too in toonuud:
        if too > max:
            max = too
    return max