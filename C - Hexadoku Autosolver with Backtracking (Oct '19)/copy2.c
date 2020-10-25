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
void copyBoard(int **startArray, int **endArray, int matrixSize);
int main(int argc, char const *argv[]){
    if (argc != 2)    {
        printf("error\n");
        return 0;
    }    else    {
        FILE *hexGrid = fopen(argv[1], "r");
        if (hexGrid == NULL)        {
            printf("error\n");
            return 0;        }
        int matrixSize = 16;
        int **hexArray = mallocMatrix(matrixSize, matrixSize); //main board
        int i, j, k;                                           //loop variables
        int failed = 0;                                        //unsolvable checker
        long num = 0;                                          //for converting char to hex
        char temp[8] = "0";                                    //extracting char from input files and not making valgrind mad for some reason
        int numEmptySlots = 0;                                 //to keep track of when the puzzle is finished
        int needToGuess = 0;                                   //keeping track of whether we're using a non count != 1 square
        int onGuessBoardRound = 0;                             //are you currently on a board made from guesses, and if so how deep into the list?
        int guessCount = 0;                                    //how to choose which number to plug into board on a guess
        int counter = 0;                                       //only do the while loop 100 times just in case of infloops
        for (i = 0; i < matrixSize; i++)        {
            for (j = 0; j < matrixSize; j++)            {
                fscanf(hexGrid, "%c\t", temp);
                if (*temp == '-')                {
                    num = matrixSize + 1; //Automatic faux EMPTY value for later checks
                    numEmptySlots++;                }
                else                    num = strtol(temp, NULL, matrixSize);
                hexArray[i][j] = num;            }        }
        fclose(hexGrid);
        int ***historyGridRecorder = malloc(numEmptySlots * sizeof(int **));
        int *historyEmptySlots = malloc(numEmptySlots * sizeof(int));
        historyGridRecorder[onGuessBoardRound] = mallocMatrix(matrixSize, matrixSize);
        copyBoard(hexArray, historyGridRecorder[onGuessBoardRound], matrixSize);
        historyEmptySlots[onGuessBoardRound] = numEmptySlots;
        onGuessBoardRound++;
        int dupeCheck = 0, row, column;
        for (row = 0; row < matrixSize; row++)        {
            for (column = 0; column < matrixSize; column++)            {
                int checkVal = hexArray[row][column];
                if (checkVal == matrixSize + 1)                    break; //value is empty, don't scan after
                for (i = column + 1; i < matrixSize; i++)                { //check the rest of the row for dupes
                    if (hexArray[row][i] == checkVal)                    {
                        dupeCheck = 1;
                        break;                    }                }
                for (i = row + 1; i < matrixSize; i++)                {
                    if (hexArray[i][column] == checkVal)                    { //check the rest of the column for dupes
                        dupeCheck = 1;
                        break;                    }                }
                if (dupeCheck)                    break;            }
            if (dupeCheck)                break;        }
        int *tempBox = malloc(matrixSize * sizeof(int));
        for (i = 0; i < matrixSize; i++)        {
            int tempCount = 0;
            for (row = 0; row < matrixSize; row++)            {
                for (column = 0; column < matrixSize; column++)                {
                    if (boxIdentifier(row, column) == i + 1)                    {
                        tempBox[tempCount] = hexArray[row][column];
                        tempCount++;                    }                }            }
            for (j = 0; j < matrixSize; j++)            {
                int checkVal = tempBox[j];
                if (checkVal == matrixSize + 1)                    break;
                for (k = j + 1; k < matrixSize; k++)                {
                    if (tempBox[k] == checkVal)                    { //check the rest of the box for dupes
                        dupeCheck = 1;
                        break;                    }                }
                if (dupeCheck)                    break;            }
            if (dupeCheck)                break;        }
        free(tempBox);
        if (dupeCheck)        {
            numEmptySlots = 0;
            failed = 1;        }
        while (numEmptySlots > 0)        {
            if (counter > 100)            {
                failed = 1;
                break;            }
            int unsolved = numEmptySlots; //Break the while loop if you scan full matrix and don't replace a value
            int *availableNumbers = malloc(sizeof(int) * matrixSize);
            for (i = 0; i < matrixSize; i++)            {
                for (j = 0; j < matrixSize; j++)                {
                    int count = 0; //reset the count for every new empty spot
                    if (hexArray[i][j] == matrixSize + 1)                    { //find avail numbers based on row/column info
                        count = checkNumbers(i, j, availableNumbers, count, hexArray);
                        if (count == 0)                        {
                            onGuessBoardRound--;
                            copyBoard(historyGridRecorder[onGuessBoardRound], hexArray, matrixSize);
                            freeMatrix(historyGridRecorder[onGuessBoardRound], matrixSize);
                            numEmptySlots = historyEmptySlots[onGuessBoardRound];
                            needToGuess = 0;
                            guessCount++;
                        }
                        else if (count == 1)                        {
                            hexArray[i][j] = availableNumbers[0];
                            numEmptySlots--;                        }
                        else if (count > 1 && needToGuess == 1)                        {
                            if (guessCount > count - 1)                                guessCount = 0;
                            hexArray[i][j] = availableNumbers[guessCount];
                            numEmptySlots--;
                            needToGuess = 0;
                            historyEmptySlots[onGuessBoardRound] = numEmptySlots;
                            historyGridRecorder[onGuessBoardRound] = mallocMatrix(matrixSize, matrixSize);
                            copyBoard(hexArray, historyGridRecorder[onGuessBoardRound], matrixSize);
                            onGuessBoardRound++;
                            guessCount++;                        }                    }                }            }
            if (unsolved == numEmptySlots)            {
                historyGridRecorder[onGuessBoardRound] = mallocMatrix(matrixSize, matrixSize);
                copyBoard(hexArray, historyGridRecorder[onGuessBoardRound], matrixSize);
                historyEmptySlots[onGuessBoardRound] = numEmptySlots;
                needToGuess = 1;
                onGuessBoardRound++;            }
            free(availableNumbers);
            counter++;        }
        if (!failed)            printMatrix(hexArray, matrixSize, matrixSize);
        else if (counter == 101)            printf("no-solution by infLoop timeout\n");
        else            printf("no-solution\n");
        freeMatrix(hexArray, matrixSize);
        for (i = 0; i < onGuessBoardRound; i++)        {
            freeMatrix(historyGridRecorder[i], matrixSize);        }
        free(historyGridRecorder);
        free(historyEmptySlots);    }
    return 0;}
int boxIdentifier(int row, int column){
    int rowChunk = (row / 4) + 1;
    int columnChunk = (column / 4) + 1;
    int boxNumber = 4 * (rowChunk - 1) + columnChunk;
    return boxNumber;}
int checkAvailableNumbers(int num, int *availableNums, int count){
    int k;
    if (count == 0)    {
        availableNums[count] = num;
        count++;    }
    else    {
        for (k = 0; k < count; k++)        {
            if (availableNums[k] == num)                break; //You found the value already, skip
            else if (k == count - 1)            { //unique value, add to the list
                availableNums[count] = num;
                count++;            }        }    }
    return count;}
int checkNumbers(int row, int column, int *availableNums, int count, int **hexArray){
    int i, j;
    for (i = 0; i < 16; i++)    { //Scan through all possible numbers
        for (j = 0; j < 16; j++)        { //check all values in the current row/column/box
            if (hexArray[row][j] == i)                break; //Number already present in row, so skip to the next
            if (hexArray[j][column] == i)                break; //Number already present in column, so skip to the next
            if (checkBoxNumbers(row, column, i, hexArray))                break; //Number already present in box, so skip to the next
            if (j == 15)            { //you didn't find the specific value, so add it to available if not a dupe
                count = checkAvailableNumbers(i, availableNums, count);            }        }    }
    return count;}
int checkBoxNumbers(int row, int column, int possVal, int **hexArray){
    int i, j, loc = 0;
    int boxLocation = boxIdentifier(row, column);
    int *tempBox = malloc(sizeof(int) * 16);
    for (i = 0; i < 16; i++)    {
        for (j = 0; j < 16; j++)        {
            if (boxIdentifier(i, j) == boxLocation)            {
                tempBox[loc] = hexArray[i][j];
                loc++;            }        }    }
    for (i = 0; i < 16; i++)    {
        if (tempBox[i] == possVal)        { //box already contains number
            free(tempBox);
            return 1;        }    }
    free(tempBox);
    return 0;}
void copyBoard(int **startArray, int **endArray, int matrixSize){
    int i, j;
    for (i = 0; i < matrixSize; i++)    {
        for (j = 0; j < matrixSize; j++)        {
            endArray[i][j] = startArray[i][j];        }    }
    return;}
int **mallocMatrix(int rows, int columns){
    int i;
    int **matrix = malloc(rows * sizeof(int *));
        for (i = 0; i < rows; i++)    {
        matrix[i] = malloc(columns * sizeof(int));    }
    return matrix;}
void freeMatrix(int **matrix, int rows){
    int i;
    for (i = 0; i < rows; i++)    {
        free(matrix[i]);    }
    free(matrix);}
void printMatrix(int **matrix, int rows, int columns){
    int i, j;
    for (i = 0; i < rows; i++)    {
        for (j = 0; j < columns; j++)        {
            printf("%X\t", matrix[i][j]);        }
        printf("\n");    }}