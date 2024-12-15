#include <stdlib.h>
#include <stdio.h>

void fn()
{
    int* x = malloc(10 * sizeof(int));
    printf("%d",*x);
    x[10] = 0;
    free(x);
}

int main()
{
    fn();
    return 0;
}