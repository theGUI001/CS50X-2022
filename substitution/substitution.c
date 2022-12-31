#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <ctype.h>

int main(int argc, string argv[])
{
    string key, plainText;
    int keyLen, plainLen;

    // check if user provided one argument (key)
    if (argc != 2)
    {
        printf("Usage: ./substitution key\n");
        return 1; // return missing key or >2 keys error
    }

    // validate key (26 unique chars, only letters)
    key = argv[1];
    keyLen = strlen(key);
    if (keyLen != 26)
    {
        printf("Key must contain 26 characters.\n");
        return 1; // return key =/= 26 chars error
    }
    for (int i = 0; i < keyLen; i++)
    {
        // verify each char is a letter
        if (!isalpha(key[i]))
        {
            printf("Usage: ./substitution key\n");
            return 1; // return bad key error
        }
        // verify each char is unique
        for (int w = i + 1; w < keyLen; w++)
        {
            if (toupper(key[i]) == toupper(key[w]))
            {
                printf("Key must contain 26 characters.\n");
                return 1; // return not unique chars error
            }
        }
    }

    // prompt for plaintext
    plainText = get_string("plaintext:  ");
    plainLen = strlen(plainText);

    for (int j = 0; j < plainLen; j++)
    {
        if (isupper(plainText[j]))
        {
            int letter = plainText[j] - 65;
            plainText[j] = toupper(key[letter]);
        }
        if (islower(plainText[j]))
        {
            int letter = plainText[j] - 97;
            plainText[j] = tolower(key[letter]);
        }
    }
    // print ciphertext
    printf("ciphertext:  %s\n", plainText);
}