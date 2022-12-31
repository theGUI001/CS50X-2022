#include <cs50.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>

bool dontHaveString(string arg);

int main(int argc, string argv[])
{
    int key = 0;
    // handle error
    if (argc != 2)
    {
        printf("Usage: ./caesar key\n");
        return 1; // return missing or too many keys error
    }

    if (dontHaveString(argv[1])) // verify if have non int chars
    {
        key = atoi(argv[1]);
    }

    if (key != 0)
    {
        string plain = get_string("plaintext:  ");
        int plainLen = strlen(plain);

        for (int i = 0; i < plainLen; i++)
        {
            if (isalpha(plain[i]))
            {
                int operation = plain[i] + (key % 26);

                if (islower(plain[i]))
                {
                    plain[i] = operation > 122 ? operation - 26 : operation; // start again after last letter
                }
                else
                {
                    plain[i] = operation > 90 ? operation - 26 : operation; // start again after last letter
                }
            }
        }
        printf("ciphertext:  %s\n", plain);
        return 0;
    }
    else
    {
        // handle error
        printf("Usage: ./caesar key\n");
        return 1;
    }
}

bool dontHaveString(string arg) // define function
{
    for (int j = 0; j < strlen(arg); j++)
    {
        if (!isdigit(arg[j]))
        {
            return false;
        }
    }
    return true;
}