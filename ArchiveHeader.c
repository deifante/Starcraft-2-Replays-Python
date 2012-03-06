#include <stdio.h>
#include <stdlib.h>

int ReadArchiveHeader(char* filepath);
int main()
{
    ReadArchiveHeader("samples/2v2.sc2replay");
    printf("Done\n");
}

int ReadArchiveHeader(char* filepath)
{
    int bytesRead = 0;
    char * magic = 0;
    FILE * inputFile = fopen(filepath, "r");
    int i=0;

    magic = calloc(4, 1);
    bytesRead = fread(magic, 1, 4, inputFile);

    for(i=0; i<4; ++i)
        printf("%d,", magic[i]);

    free(magic);
    fclose(inputFile);
    printf("Really!\n");
}
