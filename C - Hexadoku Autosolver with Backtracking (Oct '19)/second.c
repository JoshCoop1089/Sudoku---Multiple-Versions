#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <string.h>

int **mallocMatrix(int rows, int columns);
void freeMatrix(int **matrix, int rows);
void printMatrix(int **matrix, int rows, int columns);
int boxIdentifier(int row, int column);
int checkNumbers(int row, int column, int *available, int count, int **hexArray);
int checkBoxNumbers(int row, int column, int possVal, int **hexArray);
int checkAvailableNumbers(int num, int *available, int count);
void copyBoard(int ** startArray, int ** endArray, int matrixSize);

int main(int argc, char const *argv[]) {
    //Take file from argv
    if (argc != 2) {
        printf("error\n");
        return 0;
    }
    else
    {
        FILE *hexGrid = fopen(argv[1], "r");
        if (hexGrid == NULL) {
            printf("error\n");
            return 0;
        }
        int matrixSize = 16;
        int **hexArray = mallocMatrix(matrixSize, matrixSize);      //main board
        int i, j, k;                             //loop variables
        int failed = 0;                          //unsolvable checker
        long num = 0;                            //for converting char to hex
        char temp[8] = "0";                      //extracting char from input files and not making valgrind mad for some reason
        int numEmptySlots = 0;                   //to keep track of when the puzzle is finished
        int needToGuess = 0;                     //keeping track of whether we're using a non count != 1 square
        int onGuessBoardRound = 0;               //are you currently on a board made from guesses, and if so how deep into the list?
        int guessCount = 0;                      //how to choose which number to plug into board on a guess
        int counter = 0;                         //only do the while loop 100 times just in case of infloops

        //Fill the array from the text file
        for (i = 0; i < matrixSize; i++) {
            for (j = 0; j < matrixSize; j++) {
                fscanf(hexGrid, "%c\t", temp);
                if (*temp == '-') {
                    num = matrixSize + 1;                           //Automatic faux EMPTY value for later checks
                    numEmptySlots++;
                }
                else num = strtol(temp, NULL, matrixSize);
                hexArray[i][j] = num;
            }
        }
        fclose(hexGrid);

        /*Now that we know the number of empty slots, it gives us a max size
        on the number of guess boards we might need to store at the worst case*/
        int ***historyGridRecorder = malloc(numEmptySlots*sizeof(int**));
        int *historyEmptySlots = malloc(numEmptySlots*sizeof(int));
        historyGridRecorder[onGuessBoardRound] = mallocMatrix(matrixSize,matrixSize);
        copyBoard(hexArray, historyGridRecorder[onGuessBoardRound], matrixSize);
        historyEmptySlots[onGuessBoardRound] = numEmptySlots;
        onGuessBoardRound++;

        printMatrix(hexArray, matrixSize, matrixSize);
        // printf("\nStarting the solver:\n\n\tThe solved matrix is: \n\n");

        //check if the input file is valid
        //given a certain number, check the rest of the row/ column for any duplicates
        int dupeCheck = 0, row, column;
        for (row = 0; row < matrixSize; row++) {
            for (column = 0; column < matrixSize; column++) {
                int checkVal = hexArray[row][column];
                if (checkVal == matrixSize + 1) continue;              //value is empty, don't scan after
                for (i = column + 1; i < matrixSize; i++) {         //check the rest of the row for dupes
                    if (hexArray[row][i] == checkVal) {
                        // printf("duplicate value of %d at row %d column %d\n", checkVal, row, i);
                        dupeCheck = 1;
                        break;
                    }
                }
                for (i = row + 1; i < matrixSize; i++) {
                    if (hexArray[i][column] == checkVal) {          //check the rest of the column for dupes
                        // printf("duplicate value of %d at row %d column %d\n", checkVal, i, column);
                        dupeCheck = 1;
                        break;
                    }
                }
                if (dupeCheck) break;
            }
            if (dupeCheck) break;
        }

        //create a box, check the values of that box for dupes
        int *tempBox = malloc(matrixSize * sizeof(int));
        for (i = 0; i < matrixSize; i++) {
            int tempCount = 0;
            for (row = 0; row < matrixSize; row++) {
                for (column = 0; column < matrixSize; column++) {
                    if (boxIdentifier(row, column) == i + 1) {
                        // printf("%d,%d is in box %d, adding a %d to the box list\n", row, column,i, hexArray[row][column]);
                        tempBox[tempCount] = hexArray[row][column];
                        tempCount++;
                    }
                }
            }
            for (j = 0; j < matrixSize; j++) {
                int checkVal = tempBox[j];
                if (checkVal == matrixSize + 1) continue;
                // printf("Checking for dupes of %d in box %d\n", checkVal, i);
                for (k = j + 1; k < matrixSize; k++) {
                    if (tempBox[k] == checkVal) {                   //check the rest of the box for dupes
                        // printf("duplicate value of %d at box %d, %d compared to item %d\n", checkVal, i, j, k);
                        dupeCheck = 1;
                        break;
                    }
                }
                if (dupeCheck) break;
            }
            if (dupeCheck) break;
        }
        free(tempBox);

        //something is a duplicate value, immediate no solution state
        if (dupeCheck) {
            numEmptySlots = 0;
            failed = 1;
        }

        //while loop to keep track of how many spots are left open
        while (numEmptySlots > 0) {
            //For when something screws up, you might need an inf loop break
            if(counter > 100) {
                failed = 1;
                break;
            }
            int unsolved = numEmptySlots; //Break the while loop if you scan full matrix and don't replace a value
            printf("There are %d open spots left on the board in guessRound %d\n", unsolved, onGuessBoardRound);
            int *availableNumbers = malloc(sizeof(int) * matrixSize);
            for (i = 0; i < matrixSize; i++) {
                for (j = 0; j < matrixSize; j++) {
                    int count = 0;                                  //reset the count for every new empty spot
                    if (hexArray[i][j] == matrixSize + 1) {         //find avail numbers based on row/column info
                        count = checkNumbers(i, j, availableNumbers, count, hexArray);
                        // printf("\nCount of available numbers for Row %d Column %d is: %d\n", i,j,count);

                        //This would mean we've reached a point of literal impossibility, so revert back to the last guess
                        if (count == 0) {
                            onGuessBoardRound--;
                            printf("\nBoard was: \n");
                            printMatrix(hexArray,matrixSize, matrixSize);
                            printf("\n\tImpossible point, count at Row %d Column %d is 0. Reverting back to last known grid at GuessBoard %d\n", i, j, onGuessBoardRound);
                            printf("Copying from history grid\n");
                            printMatrix(historyGridRecorder[onGuessBoardRound], matrixSize, matrixSize);
                            copyBoard(historyGridRecorder[onGuessBoardRound], hexArray, matrixSize);
                            freeMatrix(historyGridRecorder[onGuessBoardRound], matrixSize);
                            printf("\tGoing from %d empty slots in GR%d ", numEmptySlots, onGuessBoardRound +1);
                            numEmptySlots = historyEmptySlots[onGuessBoardRound];
                            printf("to %d empty slots in GR %d\n",numEmptySlots, onGuessBoardRound);
                            needToGuess = 0;
                            guessCount++;
                        }

                        //purely deterministic slot
                        else if (count == 1) {
                            printf("\tReplacing the empty spot at Row %d Column %d with a %d\n", i,j,availableNumbers[0]);
                            hexArray[i][j] = availableNumbers[0];
                            numEmptySlots--;
                        }

                        //you ran out of deterministic, but can still make a guess, so save your board and try another guess
                        else if (count > 1 && needToGuess == 1) {
                            if(guessCount > count - 1) guessCount = 0;
                            printf("\nCount of available numbers for Row %d Column %d is: %d\n", i,j,count);
                            printf("\tGuessing that the spot at Row %d Column %d is a %d\n", i, j, availableNumbers[guessCount]);
                            hexArray[i][j] = availableNumbers[guessCount];
                            numEmptySlots--;
                            needToGuess = 0;
                            historyEmptySlots[onGuessBoardRound] = numEmptySlots;
                            historyGridRecorder[onGuessBoardRound] = mallocMatrix(matrixSize,matrixSize);
                            copyBoard(hexArray, historyGridRecorder[onGuessBoardRound], matrixSize);
                            printf("\t\tStored Current Board at GuessRound %d\n", onGuessBoardRound);
                            onGuessBoardRound++;
                            guessCount++;
                            
                        }
                    }
                }
            }

            if (unsolved == numEmptySlots) {
                //Here means that you have to save the board and attempt a guess
                historyGridRecorder[onGuessBoardRound] = mallocMatrix(matrixSize, matrixSize);
                copyBoard(hexArray, historyGridRecorder[onGuessBoardRound], matrixSize);
                historyEmptySlots[onGuessBoardRound] = numEmptySlots;
                needToGuess = 1;
                onGuessBoardRound++;
                printf("Reached a need to guess, board is now: \n");
                printMatrix(hexArray, matrixSize, matrixSize);
                printf("\n");
            }
            free(availableNumbers);
            counter++;
        }
        //failed will trip if you scan through and cannot replace anything, otherwise it is solved
        if (!failed) printMatrix(hexArray, matrixSize, matrixSize);
        else if(counter == 101) printf("no-solution by infLoop timeout\n");
        else printf("no-solution\n");
        freeMatrix(hexArray, matrixSize);
        for (i = 0; i < onGuessBoardRound; i++) {
            freeMatrix(historyGridRecorder[i], matrixSize);
        }
        free(historyGridRecorder);
        free(historyEmptySlots);
        
    }
    return 0;
}
/*Given a specific row/column, returns the box that location is in.  
Box numbers start in the top left, and move right
Only set up for 16x16 matrix, change if bored*/
int boxIdentifier(int row, int column) {
    int rowChunk = (row / 4) + 1;
    int columnChunk = (column / 4) + 1;
    int boxNumber = 4 * (rowChunk - 1) + columnChunk;
    return boxNumber;
}
/*Given a specific input number, compare it to the list of available numbers for a certain spot to see if it is unique*/
int checkAvailableNumbers(int num, int *availableNums, int count) {
    int k;
    if (count == 0)    {
        availableNums[count] = num;
        count++;
    }
    else {
        for (k = 0; k < count; k++) {
            // printf("starting avail number loop\n");
            if (availableNums[k] == num) break; //You found the value already, skip
            else if (k == count - 1) { //unique value, add to the list
                // printf("found a unique value\n");
                availableNums[count] = num;
                count++;
            }
        }
    }
    return count;
}
/*Check row/column/box of a given space for available numbers, only works for 16x16 matrix, change to make it modular if bored*/
int checkNumbers(int row, int column, int *availableNums, int count, int **hexArray) {
    int i, j;
    for (i = 0; i < 16; i++) {                                      //Scan through all possible numbers
        for (j = 0; j < 16; j++) {                                  //check all values in the current row/column/box
            if (hexArray[row][j] == i) break;                       //Number already present in row, so skip to the next
            if (hexArray[j][column] == i) break;                    //Number already present in column, so skip to the next
            if (checkBoxNumbers(row, column, i, hexArray)) break;   //Number already present in box, so skip to the next
            if (j == 15) {                                          //you didn't find the specific value, so add it to available if not a dupe
                // printf("%d not present in row/column/box for %d,%d\n", i, row, column);
                count = checkAvailableNumbers(i, availableNums, count);
            }
        }
    }
    return count;
}
/*Calculate the numbers in a specific box given a row/colun value, and checks if a number is already a member of that box
Only works for 16x16 matrix, change if bored*/
int checkBoxNumbers(int row, int column, int possVal, int **hexArray) {
    int i, j, loc = 0;
    int boxLocation = boxIdentifier(row, column);
    int *tempBox = malloc(sizeof(int) * 16);
    //run through the full array making a temp list of numbers in the current box
    for (i = 0; i < 16; i++) {
        for (j = 0; j < 16; j++) {
            if (boxIdentifier(i, j) == boxLocation) {
                tempBox[loc] = hexArray[i][j];
                loc++;
            }
        }
    }
    for (i = 0; i < 16; i++) {
        if (tempBox[i] == possVal) { //box already contains number
            free(tempBox);
            return 1;
        }
    }
    //If you get here, the possible value is not in the current box
    free(tempBox);
    return 0;
}
/*Stores the current layout of a board in a different array to be refered to later*/
void copyBoard(int ** startArray, int ** endArray, int matrixSize) {
    int i,j;
    for(i = 0; i < matrixSize; i++) {
        for (j = 0; j < matrixSize; j++) {
            endArray[i][j] = startArray[i][j];
        }
    }
    return;
}
/* 2dmatrix malloc function with row,column as input */
int **mallocMatrix(int rows, int columns) {
    int i;
    int **matrix = malloc(rows * sizeof(int *));
    for (i = 0; i < rows; i++) {
        matrix[i] = malloc(columns * sizeof(int));
    }
    return matrix;
}
/*Assuming a 2d array of ints*/
void freeMatrix(int **matrix, int rows) {
    int i;
    for (i = 0; i < rows; i++) {
        free(matrix[i]);
    }
    free(matrix);
}
/*Assuming a 2d array of ints with the output values printed in hexadecimal base*/
void printMatrix(int **matrix, int rows, int columns) {
    int i, j;
    for (i = 0; i < rows; i++) {
        for (j = 0; j < columns; j++) {
            printf("%X\t", matrix[i][j]);
        }
        printf("\n");
    }
}