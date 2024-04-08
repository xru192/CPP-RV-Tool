/***
This is a example that match the read after close . 
***/
#include<stdio.h>
#include<stdlib.h>
int main()
{
    FILE *fp;
    char* filePath="input.txt";
    fp= fopen(filePath,"r");
    if (fp!=NULL)
    {
        while (!feof(fp))
            printf("%c", fgetc(fp));
    } else{
        printf("fail to open\n");
    }
    fclose(fp);
    printf("%c", fgetc(fp));
}
