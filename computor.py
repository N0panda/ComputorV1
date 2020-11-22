import sys
import argparse
import re
from core.Parsing import ft_return_error, ft_parse_token, ft_get_sign, ft_calcul_side, ft_merge_sign, ft_reduced_form, ft_get_max_degree, ft_equation_to_str, ft_zero_filter, ft_get_discriminant
from core.Parsing import solutions_for_x1, solutions_for_x2

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process a polinomial equation')
    parser.add_argument("equation", help="enter an unique string as the the equation")
    args = parser.parse_args()

    raw_str = args.equation
    splitted = raw_str.split("=")

    if len(splitted := raw_str.split("=")) < 2:
        ft_return_error(None, error=1)
    if len(splitted) > 2:
        ft_return_error(None, error=3)
    if len(splitted[1].strip()) < 1 or len(splitted[0].strip()) < 1:
        ft_return_error(None, error=4)
    left = re.split(r"[+-]", splitted[0])
    right = re.split(r"[+-]", splitted[1])
    left = list(map(str.strip, left))
    right = list(map(str.strip, right)) 

    #### Gros parsing avec Regex
    left = ft_parse_token(left)
    right = ft_parse_token(right)

    #### Recuperation des + et -
    sign_left = ft_get_sign(splitted[0], len(left))
    sign_right = ft_get_sign(splitted[1], len(right))

    #### Fusion des signes et des valeurs sous forme [valeur, exposant]
    left = ft_merge_sign(sign_left, left)
    right = ft_merge_sign(sign_right, right)

    #### Récuperation du degré
    degree = ft_get_max_degree([left, right])

    #### Resolution de chaque côtés d'équation
    left = ft_calcul_side(left)
    right = ft_calcul_side(right)

    #### Gestion des cas ou on a degree==0 donc seulement des reels
    # if degree == 0 and left[0][0] - right[0][0] == 0:
    #     print("All Real numbers are solutions")
    #     sys.exit()
    if degree == 0 and left[0][0] - right[0][0] != 0:
        print("There are no Real solutions")
        sys.exit()
    if len(right) == len(left):
        check = 0
        for i in range(len(right)):
            if left[i][0] != right[i][0]:
                check = 1
        if check == 0:
            print("All Real numbers are solutions")
            sys.exit()


    reduced = ft_reduced_form(left, right)

    new_degree = ft_get_max_degree([reduced])

    if new_degree == 0:
        if reduced[0][0] == 0.0:
            print("All Real numbers are solutions")
            sys.exit()
        else :
            print("There are no Real solutions")
            sys.exit()
    discriminant = ft_get_discriminant(reduced) if new_degree == 2 else None


    print("\n* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *")
    print("\nThe Polynomial degree Before reduction is  --> ", degree)
    print("The Polynomial degree After reduction is   --> ", new_degree)
    print("The reduced form is :\n", ft_equation_to_str(reduced))
    print("")
    if new_degree == 1:
        solutions_for_x1(reduced)
    elif new_degree == 2:
        solutions_for_x2(reduced)
    else:
        print("This program can only solve Polynomes of degree 2")
        sys.exit()
    print("\n* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *\n")