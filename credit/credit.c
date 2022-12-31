#include <cs50.h>
#include <stdio.h>
#include <math.h>
#include <stdlib.h>

int get_n_digits(float number); // custom function prototype

int main(void)
{
    long long ccNumber;
    int nDigits, dSum, sum;

    ccNumber = get_long_long("Card Number: "); // prompt for card number
    nDigits = get_n_digits(ccNumber);          // count how many digits the number have

    if (nDigits < 13 || nDigits > 16) // validate input
    {
        printf("INVALID\n");
        return 0;
    }

    // Create array with card digits
    long long cDigits[nDigits];

    for (int i = (nDigits - 1); i >= 0; i--)
    {
        cDigits[i] = ccNumber % 10;
        ccNumber = floor(ccNumber / 10);
    }

    // starting Luhn's algorithm
    long long doubleDigits[nDigits];

    for (int w = (nDigits - 2), l = 0; w >= 0; w -= 2, l++) // get numbers to double
    {
        doubleDigits[l] = cDigits[w] * 2;
    }

    // sum double numbers
    for (int s = 0; s <= ((nDigits - 2) / 2); s++)
    {
        if (doubleDigits[s] > 9)
        {
            dSum = dSum + (floor(doubleDigits[s] / 10)) + (doubleDigits[s] % 10);
        }
        else
        {
            dSum = dSum + doubleDigits[s];
        }
    }

    // sum other digits
    sum = 0;

    for (int k = nDigits - 1; k >= 0; k -= 2)
    {
        int nonDouble = cDigits[k];
        sum = sum + nonDouble;
    }

    // verify card
    if ((sum + dSum) % 10 == 0)
    {
        switch (cDigits[0])
        {
            case 3: // verify if is an Amex card
                if (cDigits[1] == 4 || cDigits[1] == 7)
                {
                    printf("AMEX\n");
                }
                else
                {
                    printf("INVALID\n");
                }
                break;

            case 4: // verify if is an Visa card
                printf("VISA\n");
                break;

            case 5: // verify if is an Master card
                if (cDigits[1] == 1 || cDigits[1] == 2 || cDigits[1] == 3 || cDigits[1] == 4 || cDigits[1] == 5)
                {
                    printf("MASTERCARD\n");
                }
                else
                {
                    printf("INVALID\n");
                }
                break;
        }
    }
    else
    {
        printf("INVALID\n");
    }
}

int get_n_digits(float number) // custom function definition
{
    return floor(log10(fabs(number))) + 1;
}