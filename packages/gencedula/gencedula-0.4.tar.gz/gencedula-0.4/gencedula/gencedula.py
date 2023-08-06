#!/usr/bin/env python3

from secretsrandrange import randrange


def get_verifier_digit(cedula: int) -> int:
    """
    Get verifier digit of uruguayan identification document.
    https://es.wikipedia.org/wiki/C%C3%A9dula_de_Identidad_de_Uruguay
        #D%C3%ADgito_verificador
    (spanish article).

    :param cedula: int: Identification number without verifier digit.

    """
    cedula_string = str(cedula).zfill(7)
    return (
        10
        - (
            (
                int(cedula_string[0]) * 2
                + int(cedula_string[1]) * 9
                + int(cedula_string[2]) * 8
                + int(cedula_string[3]) * 7
                + int(cedula_string[4]) * 6
                + int(cedula_string[5]) * 3
                + int(cedula_string[6]) * 4
            )
            % 10
        )
    ) % 10


def generate_cedula(
    start: int = 0,
    stop: int = 10_000_000,
    step: int = 1
        ) -> int:
    """
    Get a random uruguayan identity document.
    :param start: int: Start number.  (Default value = 0)
    :param stop: int: Stop number. (Default value = 4_999_999)
    :param step: int: Step. (Default value = 0)

    """
    if start < 0 or stop > 10_000_000:
        raise ValueError("Cedula values have to be between 0 and 10 000 000.")

    cedula = randrange(start=start, stop=stop, step=step)
    return int(f"{cedula}{get_verifier_digit(cedula)}")
