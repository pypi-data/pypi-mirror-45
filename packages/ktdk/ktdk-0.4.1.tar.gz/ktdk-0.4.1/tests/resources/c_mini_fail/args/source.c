#include <stdio.h>
#include <string.h>
#define BUFFER_SIZE 256

int main(int argc, char **argv) {

    for(int i = 1; i < argc; i++) {
        if(strlen(argv[i])){
            puts(argv[i]);
        }
    }

    return 0;
}

