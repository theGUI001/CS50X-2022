#include <cs50.h>
#include <stdio.h>

int main(void)
{
    int height, column, row, space;
    do // prompt for height
    {
        height = get_int("Height (1 to 8 values only): ");
    }
    while (height < 1 || height > 8); // validate height

    for (row = 0; row < height; row++)
    {
        for (space = 0; space < height - row - 1; space++) // makes spacing right for first side
        {
            printf(" ");
        }

        for (column = 0; column <= row; column++) // fisrt column
        {
            printf("#");
        }
        printf("  ");

        for (column = 0; column <= row; column++) // second column
        {
            printf("#");
        }
        printf("\n");
    }
}