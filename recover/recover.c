#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

typedef uint8_t BYTE;
int char_size = sizeof(char);

int main(int argc, char *argv[])
{
    if (argc != 2) // verify if provided only one argument
    {
        printf("Usage: ./recover IMAGE\n");
        return 1;
    }

    FILE *recover = fopen(argv[1], "r"); // open file to recover
    if (recover == NULL)                 // if file is invalid return 1
    {
        printf("Could not open file.\n");
        return 1;
    }

    BYTE buffer[512]; // create buffer
    int images = 0;   // counter of images
    FILE *out = NULL; // output file
    char *filename = malloc(8 * char_size);

    // read all blocks
    while (fread(buffer, char_size, 512, recover))
    {
        // check if is the start of a JPEG
        if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff && (buffer[3] & 0xf0) == 0xe0)
        {
            if (images > 0) // close output files
            {
                fclose(out);
            }

            sprintf(filename, "%03i.jpg", images); // write file names
            out = fopen(filename, "w");            // open output

            images++;
        }
        if (out != NULL)
        {
            fwrite(buffer, char_size, 512, out); // write JPEG to file
        }
    }
    free(filename);
    fclose(recover);
    fclose(out);

    return 0;
}