def main():
    ccNumber = input("Card Number: ")
    nDigits = len(ccNumber)

    # Validate if valid number of digits
    if nDigits < 13 or nDigits > 16:
        print("INVALID")
        exit()

    if (luhns(ccNumber) == 0):
        brand(digitsOf(ccNumber))
    else:
        print("INVALID")


def digitsOf(x):
    return [int(d) for d in str(x)]


def luhns(card):
    # String to array with digitss
    digits = digitsOf(card)
    # Get the odd and even digits
    oddD = digits[-1::-2]
    evenD = digits[-2::-2]

    # Calculate checksum
    checksum = 0
    checksum += sum(oddD)

    for d in evenD:
        checksum += sum(digitsOf(d * 2))

    return checksum % 10


def brand(card):
    # Verify if is amex
    if card[0] == 3 and card[1] == 4 or card[1] == 7:
        print("AMEX")

    # Verify if is visa
    elif card[0] == 4:
        print("VISA")

    # Verify if is mastercard
    elif card[0] == 5 and (0 < card[1] <= 5):
        print("MASTERCARD")

    else:
        print("INVALID")


main()
