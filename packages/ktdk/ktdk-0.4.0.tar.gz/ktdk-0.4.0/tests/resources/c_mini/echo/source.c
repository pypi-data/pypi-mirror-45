#include <stdio.h>
#define BUFFER_SIZE 256

int main(void) {

    char buffer[BUFFER_SIZE];
    fgets(buffer, BUFFER_SIZE - 1, stdin);
    printf(buffer);

    return 0;
}

