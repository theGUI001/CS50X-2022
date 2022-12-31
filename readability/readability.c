#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <ctype.h>
#include <math.h>

int main(void)
{
    string text = get_string("Text: ");
    int textLen = strlen(text);
    int words = 1;
    int letters = 0;
    int sentences = 0;
    int index;
    float l, s;

    for (int i = 0; i < textLen; i++)
    {
        // count letters
        if (isalnum(text[i]))
        {
            letters += 1;
        }
        // count words
        if (text[i] == ' ')
        {
            words += 1;
        }
        // count sentences
        if (text[i] == '.' || text[i] == '!' || text[i] == '?')
        {
            sentences += 1;
        }
    }

    // do the Coleman-Liau index
    l = (float)letters / words * 100;
    s = (float)sentences / words * 100.0;
    index = round(0.0588 * l - 0.296 * s - 15.8);

    // verify grades and output
    if (index < 1)
    {
        printf("Before Grade 1\n");
        return 0;
    }
    if (index >= 16)
    {
        printf("Grade 16+\n");
        return 0;
    }

    printf("Grade %i\n", index);
}