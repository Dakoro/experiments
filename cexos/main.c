#include <stdio.h>

struct X
{
    short s; 
    int i; 
    char c;
};

struct Y
{
    int i;
    char c;
    short s;
};

struct Z
{
    int   i;
    short s;
    char  c;
};

int main() {
    printf("%ld", sizeof(short)+sizeof(int)+sizeof(char));
}