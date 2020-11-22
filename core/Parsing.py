import sys
import re
import math

def ft_return_error(bad_elem, error):
    if error == 1: print("Its not an equation ... \'=\'")
    elif error == 2: print("Bad formated element : ", bad_elem[0])
    elif error == 3: print("Equation with more than One \'=\' ? nevermind ")
    elif error == 4: print("Enter at least one character after the \'=\' ?")
    elif error == 5: print(bad_elem[0], " is a bit too much isn\'t it ?")
    sys.exit()

def ft_parse_token(token):
    parsed_token = []
    i = 0
    for tok in token:
        tmp = tok.replace(" ", "")
        if i == 0 and len(tmp) == 0:
            pass
        elif re.match(r'^\d+(?:\.\d+)?\*?[Xx](\^?\d+)?$',tmp): #### cas ou on a un multiplicateur  et X
            split_on_x = tmp.replace("x", "X").split('X')
            multiplicateur = float(re.search(r'\d+(?:\.\d+)?', split_on_x[0])[0])
            exposant_raw = re.search(r'\d+', split_on_x[1])
            exposant = int(exposant_raw[0]) if exposant_raw is not None else 1
            if int(exposant) > 99:
                ft_return_error([str(exposant_raw[0])],error=5)
            parsed_token.append((multiplicateur, exposant))
            
        elif re.match(r'^\d+(?:\.\d+)?(\*?[xX](\^?\d)?)?$', tmp): #### cas ou on a un multiplicateur
            multiplicateur = float(tmp)
            parsed_token.append((multiplicateur,0))

        elif re.match(r'^[Xx](\^?\d+)?$', tmp): #### cas avec X seul
            exposant_raw = re.search(r'\d+', tmp)
            exposant = int(exposant_raw[0]) if exposant_raw is not None else 1
            if int(exposant) > 99:
                ft_return_error([str(exposant_raw[0])],error=5)
            parsed_token.append((1.0,exposant))

        else :
            ft_return_error([tmp], 2)
        i +=1
    return parsed_token

def ft_get_max_degree(arrs):
    dmax = 0

    for arr in arrs:
        for item in arr:
            dmax = item[1] if dmax < item[1] and item[0] != 0 else dmax
    return dmax

def ft_get_sign(s, length):
    sign_tab = []
    nb = 0
    for c in s[::-1]:
        if c == '+' or c == '-':
            sign_tab.append(c)
            nb +=1
    if length != nb:
        sign_tab.append('+')
    return sign_tab[::-1]

def ft_merge_sign(sign_tab, side):
    merged = []
    for sign, poly in zip(sign_tab, side):
        merged.append([float(sign + str(poly[0])), poly[1]])
    return merged

def ft_calcul_side(side):
    i = 0
    result = []
    while(i < ft_get_max_degree([side]) + 1):
        val = float(sum([x for x,y in side if y == i]))
        val = [val, i]
        result.append(val)
        i += 1
    return result

def ft_zero_filter(equation):
    for item in equation[1:][::-1]:
        if item[0] == 0: equation.pop()
        else : break
    return equation

def ft_reduced_form(left, right):
    for item in right:
        item[0] *= -1
        left.append(item)
    result = ft_calcul_side(left)
    result = ft_zero_filter(result)
    return result

def ft_equation_to_str(equation):
    result = ""
    i = 0
    for elem in equation:
        value = elem[0]
        if value >= 0 : sign = "+"
        else :
            sign = "-"
            value *= -1

        if i == 0 and sign == "+": sign = ""
        tmp = sign + " " + str(value) + " * X^" + str(elem[1]) + " "
        result += tmp
        i += 1
    result += "= 0"
    return result

def    ft_get_discriminant(equation):
    a = equation[2][0]
    b = equation[1][0]
    c = equation[0][0]

    discriminant = (b ** 2) - (4 * a * c)
    return discriminant

def solutions_for_x1(equation):
    poly = equation[1][0]
    real = equation[0][0]
    x = (-1 * real) / poly
    
    print("The solution is :\n", x)


def solutions_for_x2(equation):
    discriminant = ft_get_discriminant(equation)
    a = equation[2][0]
    b = equation[1][0]
    c = equation[0][0]

    if discriminant < 0:
        print("Discriminant is < 0 : There is no real solutions")
        l = (-1 * b) / (2 * a)
        r = math.sqrt((-1) * discriminant) / (2 * a)
        if r < 0:
            r = r * (-1)
        x1 = str(l) + " + i * " + str(r)
        x2 = str(l) + " - i * " + str(r)
        print("The Two complexes solutions are :\n x1 = ", x1, "\n x2 = ", x2)

    elif discriminant == 0:
        x = -1 * (b / (2 * a))
        print("Discriminant is == 0 : The solution is :\nx = ", x)

    else:
        x1 = ((-1 * b) - math.sqrt(discriminant)) / (2 * a)
        x2 = ((-1 * b) + math.sqrt(discriminant)) / (2 * a)
        print("Discriminant is > 0 : The Two solutions are :\n x1 = ", x1, "\n x2 = ", x2)
