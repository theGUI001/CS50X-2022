#include <stdio.h>
#include <cs50.h>

int main(void)
{
    string name = get_string("What's your name? "); // get prompt for name
    printf("Hello, %s\n", name);                    // print hello + name
}