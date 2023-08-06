def c_to_f(celsius):
    value = celsius
    fstval = 9 / 5
    scdval = fstval * value
    fnlval = scdval + 32
    return fnlval

def f_to_c(fahrenheit):
    value = fahrenheit
    fstval = 5 / 9
    scdval = fahrenheit -32
    fnlval = fstval * scdval
    return fnlval

def me_to_ce(meter):
    value = meter
    fnlval = meter * 100
    return fnlval

def ce_to_me(centimeter):
    value = centimeter
    fnlval = centimeter / 100
    return fnlval

def me_to_km(meter):
    value = meter
    fnlval = meter / 1000
    return fnlval

def km_to_me(km):
    value = km
    fnlval = km * 1000
    return fnlval

def me_to_fe(meter):
    value = meter
    fnlval = meter * 3.28084
    return fnlval

def fe_to_me(feet):
    value = feet
    fnlval = feet / 3.28084
    return fnlval
