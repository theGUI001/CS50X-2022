// Implements a dictionary's functionality

#include <ctype.h>
#include <stdbool.h>
#include <string.h>
#include <stdlib.h>
#include <stdio.h>
#include <strings.h>

#include "dictionary.h"

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
} node;

const int nodeSize = sizeof(node);

// Choose number of buckets in hash table
const unsigned int N = 26;

// Hash table
node *table[N];

unsigned int word_count, hashV;

// Returns true if word is in dictionary, else false
bool check(const char *word)
{
    hashV = hash(word);
    node *cursor = table[hashV];

    while (cursor != 0)
    {
        if (strcasecmp(word, cursor->word) == 0)
        {
            return true;
        }
        cursor = cursor->next;
    }

    return false;
}

// Hashes word to a number
unsigned int hash(const char *word)
{
    unsigned long total = 0;
    for (int i = 0, wordLen = strlen(word); i < wordLen; i++)
    {
        total += tolower(word[i]);
    }
    return total % N;
}

// Loads dictionary into memory, returning true if successful, else false
bool load(const char *dictionary)
{
    // load file
    FILE *file = fopen(dictionary, "r");

    if (file == NULL) // verify if dictionary is valid
    {
        printf("Unable to open the file.");
        return false;
    }

    char word[LENGTH + 1];

    // scan dictionary for words
    while (fscanf(file, "%s", word) != EOF)
    {
        // aloc memory
        node *n = malloc(nodeSize);
        if (n == NULL) // verify if computer have memory
        {
            return false;
        }

        // cpy word to node
        strcpy(n->word, word);
        hashV = hash(word);
        n->next = table[hashV];
        table[hashV] = n;
        word_count++;
    }
    fclose(file);
    return true;
}

// Returns number of words in dictionary if loaded, else 0 if not yet loaded
unsigned int size(void)
{
    if (word_count > 0)
    {
        return word_count;
    }
    return 0;
}

// Unloads dictionary from memory, returning true if successful, else false
bool unload(void)
{
    for (int i = 0; i < N; i++)
    {
        node *cursor = table[i];
        while (cursor != NULL)
        {
            node *tmp = cursor;
            cursor = cursor->next;
            free(tmp);
        }
        if (cursor == NULL && i == N - 1)
        {
            return true;
        }
    }
    return false;
}
