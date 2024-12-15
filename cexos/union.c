#include <stdio.h>

union byte_set{
    int x;
    unsigned char tab[4];
};

int main() {

    union byte_set number;
    number.x = 1000;
    for (int i=0; i<4; i++) {
        printf("%d ", number.tab[i]);
    }

    return 0;
}