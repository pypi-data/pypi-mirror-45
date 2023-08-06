import leapyear

def get(year):
    year = int(year)
    if leapyear.get(year):
        return 366
    else:
        return 365
