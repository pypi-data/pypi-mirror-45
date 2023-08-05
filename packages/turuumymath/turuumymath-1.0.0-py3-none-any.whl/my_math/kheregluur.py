def max_olokh(toonuud):
    max = toonuud[0]
    for too in toonuud:
        max = int(max) if int(too) <= int(max) else int(too)

    return max
