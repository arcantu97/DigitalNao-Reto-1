def lower_number_word(word: str) -> str:
    """
    This function takes the first letter from the word
    and lower case it.
    """
    return word[0].lower() + word[1:]


def rename_base_two(word: str) -> str:
    """
    This function takes the **number** (word) and replaces the last letter
    with letter i, as base from spanish language.
    """
    return word[:-1] + 'i'


class NumberToWords:

    def __init__(self):
        self.baseNumber = [
            "Cero", "Uno", "Dos", "Tres", "Cuatro", "Cinco",
            "Seis", "Siete", "Ocho", "Nueve", "Diez", "Once",
            "Doce", "Trece", "Catorce", "Quince", "Dieciséis",
            "Diecisiete", "Dieciocho", "Diecinueve", "Veinte"]

        self.base10 = [
            "Veinte", "Treinta", "Cuarenta", "Cincuenta",
            "Sesenta", "Setenta", "Ochenta", "Noventa", "Cien"]

    def convert(self, number: int) -> str:
        if number <= 20:
            result = self.baseNumber[number]
        else:
            number_length = len(str(number))
            if number_length > 2:
                first_number = self.base10[-1]
                second_number = int(str(number)[1])
                third_number = int(str(number)[2])
                concatenated_number = int(str(second_number) + str(third_number))
                if concatenated_number <= 20:
                    result = "{}to {}".format(first_number, self.baseNumber[concatenated_number])
                else:
                    second_number = self.base10[int(str(number)[1]) - 2]
                    third_number = self.baseNumber[int(str(number)[2])]
                    if int(str(number)[1]) == 2:
                        result = "{}to {}{}".format(
                            first_number,
                            rename_base_two(second_number),
                            lower_number_word(third_number)
                        )
                    elif int(str(number)[2]) == 0:
                        result = "{}to {}".format(
                            first_number,
                            lower_number_word(second_number)
                        )
                    else:
                        result = "{}to {} y {}".format(
                            first_number,
                            lower_number_word(second_number),
                            lower_number_word(third_number))
            else:
                first_number = int(str(number)[0])
                second_number = self.baseNumber[int(str(number)[1])]
                result = "{} y {}".format(
                    self.base10[first_number - 2],
                    lower_number_word(second_number))

        return result
