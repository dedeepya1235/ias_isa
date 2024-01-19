#include<stdio.h>

void main(){
    int arr[11];
    arr[1] = 65;
    arr[2] = 24;
    arr[3] = 75;
    arr[4] = 49;
    arr[5] = 101;
    arr[6] = 81;
    arr[7] = 43;
    arr[8] = 57;
    arr[9] = 2;
    arr[10] = 97;

    for(int i=2; i<=10; i++){
        int temp = arr[i];
        int j = i-1;
        while(j>=1 && arr[j] > temp){
            arr[j+1] = arr[j];
            j--;
        }
        arr[j+1] = temp;
    }

    printf("%d\n%d\n%d\n%d\n%d\n%d\n%d\n%d\n%d\n%d\n", arr[1], arr[2]
    , arr[3], arr[4], arr[5], arr[6], arr[7], arr[8], arr[9], arr[10]);
}