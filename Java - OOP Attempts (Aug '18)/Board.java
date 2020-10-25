/**
 * @Author: Josh Cooper
 * @Date:   2018-10-24T08:57:47-04:00
 * @Filename: board.java
 * @Last modified by:   Josh Cooper
 * @Last modified time: 2018-11-27T19:41:45-05:00
 * Java Changes relative to Python v3b
 *    Updated to OOP for practice manipulating personal class object
 *    Switched history recorder from quadratic to linear
 */


import java.util.*;
public class Board {

  //Attributes
  private int num;  //will be required for calculating certain properties for box choice
  private int gameCount = 1; //Used to access specific game moves for Undo function
  private String boardFileName; // for accessing the specific file with required boards

    //Used in Sudoku.java while loops for proper row/column checks
  private boolean isRowChosen = false;
  private boolean isColumnChosen = false;
  private boolean isNumberChosen = false;

    //Setting up the board arrays for restarting game and managing current board
  private int[][] startBoard;  // should be filled in by FileIO from the premade text files eventually
  private int[][] currentBoard;  // will hold the currentBoard version of the board
  private HashMap<String, int[]> boardState = new HashMap<String, int[]>(); //Unique checks rely on keys stored here
  private HashMap<Integer, String> gameHistory = new HashMap<Integer, String>(); //Undo function relies on Strings stored here


  //Constructor
  public Board(int size, char difficulty) {
    this.num = (int) Math.pow(size, 0.5);
    this.startBoard = new int[size][size];
    this.currentBoard = new int[size][size];
    String diffWord = "";
    if (difficulty == 'e') {
      diffWord = " Easy.txt";
    } else if (difficulty == 'm') {
      diffWord = " Medium.txt";
    } else if (difficulty == 'h') {
      diffWord = " Hard.txt";
    } else if (difficulty == '_') {
      diffWord = ".txt";
    }
    this.boardFileName = size + "x" + size + diffWord;
  }

  //Getters
  public int[][] getStartBoard() {
    return this.startBoard;
  }
  public int[] getBoardState(String key) {
    return this.boardState.get(key);
  }
  public int getCurrentBoardNumber(int row, int column) {
    return this.currentBoard[row-1][column-1];
  }
  public int getGameCount() {
    return this.gameCount;
  }
  public String getGameHistory(int num) {
    return this.gameHistory.get(num);
  }
  public boolean getIsRowChosen() {
    return this.isRowChosen;
  }
  public boolean getIsColumnChosen() {
    return this.isColumnChosen;
  }
  public boolean getIsNumberChosen() {
    return this.isNumberChosen;
  }
  public int getNum() {
    return this.num;
  }
  public String getBoardFileName() {
    return this.boardFileName;
  }


  //Setters
  public void setIsRowChosen(boolean rowChosen) {
    this.isRowChosen = rowChosen;
  }
  public void setIsColumnChosen(boolean columnChosen) {
    this.isColumnChosen = columnChosen;
  }
  public void setIsNumberChosen(boolean numberChosen) {
    this.isNumberChosen = numberChosen;
  }
  public void setCurrentBoardNumber(int row, int column, int number) {
    this.currentBoard[row-1][column-1] = number;
  }

  	//This should modify specific keys to update the state when you plug in new numbers
  public void setBoardState(String key, int[] nums) {
    this.boardState.put(key,nums);
  }
    //This should store a move as a string and allow us to refer to later via undo function
  public void setGameHistory(String lastMove) {
    this.gameHistory.put(this.getGameCount(),lastMove);
  }



  //Methods To Finish

  public static void chooseRandomBoard () {}
  public void undoMove() {
    System.out.println("The board will now be:\n");
    this.gameCount--;
    // this.currentBoard = this.gameHistory.get(this.gameCount);
    this.boardPrint();
  }
  public int getLastMoveOriginalNum(String lastMove) {
    int origNum = Integer.parseInt(lastMove.substring(9,10));
    return origNum;
  }
  public int getLastMoveOriginalRow(String lastMove) {
    int origRow = Integer.parseInt(lastMove.substring(18,19));
    return origRow;
  }
  public int getLastMoveOriginalColumn(String lastMove) {
    int origColumn = Integer.parseInt(lastMove.substring(27,28));
    return origColumn;
  }
  public int getLastMoveNewNumber(String lastMove) {
    int newNumber = Integer.parseInt(lastMove.substring(34,35));
    return newNumber;
  }

  //Complete Methods
  public void boardPrint() {
    int count = 0;
    int columnHold = 1;
    int columnCount = 0;
    int rowShow = 1;
    String rowOut = "";
    int dashCount = this.num*(3*this.num+3)+1;

    //Create Column Numbers for Header
    Map<Integer, String> columnMap = new HashMap<>();
    while (columnCount < this.getNum()) {
      String columns = "";
      for (int i = columnHold; i < columnHold + num; i++) {
        columns += i + "  ";
      }
      columnMap.put(columnCount,columns);
      columnHold += num;
      columnCount++;
    }
    String columnList = "";
    for (int key: columnMap.keySet()) {
            columnList +=  columnMap.get(key) + "   ";
    }

    //Board Header
    String space = "";
    for(int i = 0; i < dashCount/2; i++) {
      space += " ";
    }
    String dashes = "";
    for (int i = 0; i < dashCount; i++) {
      dashes += "-";
    }
    System.out.println(space + "  Column #");
    System.out.println("||Row   " + columnList);
    System.out.println("\\/ # " + dashes);

    //Internal Board Parts
    Map<Integer, String> boardChunk = new HashMap<>();
    int numHold = 0;
    for (int i = 0; i < this.currentBoard.length; i++) {
      numHold = 0;
      for (int j = 0; j < num; j++) {
        boardChunk.put(count,Arrays.toString(Arrays.copyOfRange(this.currentBoard[i],numHold, num + numHold)));
        count++;
        numHold += num;
      }
    }
    numHold = 0;
    while (rowShow <= this.currentBoard.length) {
      for (int i = numHold; i < num + numHold; i++) {
        rowOut += " | " + boardChunk.get(i);
      }
      System.out.println("   " + Integer.toString(rowShow) + rowOut + " |");
      numHold += num;
      rowShow++;
      rowOut = "";
      if (rowShow%num == 1) {
        System.out.println("     " + dashes);
      }
    }
  }
  public static String chooseBoardSizeAndDifficulty() {
    Set<Integer> sizeSet = new HashSet<Integer>();
    sizeSet.add(4);
    sizeSet.add(9);
    sizeSet.add(99);
    int size = 0;
    // try {
      System.out.print("Please pick which type of board you want to play."+
                        "\n\tInput 4 for a 4x4 game, or 9 for a 9x9 game."+
                        "\n\tInput 99 to quit. ===> ");
//      size = input.nextInt();
      if (!sizeSet.contains(size)) {
        //spit out an exception;
      }
      if (size == 99) {
        return "";
      }
      if (size == 4) {
        return "4";
      } else {
        String diff = chooseDifficulty();
        if (diff.equals("-")) {
          return "";
        } else {
          return "9" + diff;
        }
      }
    // }
    // catch (Exception e) {
    //
    // }
  }
  public static String chooseDifficulty() {
    Set<String> difficultySet = new HashSet<String>();
    difficultySet.add("e");
    difficultySet.add("m");
    difficultySet.add("h");
    difficultySet.add("q");
    String difficulty = "";
    // try {
      System.out.print("What level difficulty would you like to try?"+
                              "\n\tInput e for easy, m for medium, or  h for hard."+
                              "\n\tInput q to quit. ===> ");
 //     difficulty = input.next();
      if (!difficultySet.contains(difficulty)) {
        //spit out error
      }
      if (difficulty.equals("q")) {
        return "-";
      } else {
        return difficulty;
      }
    //
    // } catch (Exception e) {
    //
    // }
  }
  public static Board boardStart() {
    //load board from file, populate this.startBoard with proper digits,
    // populate this.boardState with first set of row,column,box values
    String boardSizeAndDifficulty = chooseBoardSizeAndDifficulty();
    if (boardSizeAndDifficulty.length() == 0) {
      System.out.println("Guess we aren't playing after all!");
      return null;
    }
    char difficulty = '_';
    int size = Integer.parseInt(boardSizeAndDifficulty.substring(0,1));
    if (boardSizeAndDifficulty.length() > 1) {
      difficulty = boardSizeAndDifficulty.charAt(1);
    }
    Board startBoard = new Board(size, difficulty);
    return startBoard;
  }
  public void startBoardState() {

    this.currentBoard[1][1] = 2;
    this.currentBoard[0][2] = 4;
    this.currentBoard[3][3] = 6;
    this.currentBoard[2][0] = 8;
    this.currentBoard[2][1] = 2;
    this.currentBoard[0][3] = 4;
    this.currentBoard[2][3] = 6;
    this.currentBoard[1][3] = 8;

    //Internal helper for box aggregation
    HashMap<String, List<Integer>> boxes= new HashMap<>();
    List<Integer> boxHelper = new ArrayList<>();
    //Iterate over tihs.current to create inital values for row,column and box
    for (int i = 0; i < this.currentBoard.length; i++) {
      boardState.put("Row " + Integer.toString(i+1), this.currentBoard[i]); //Row Creator
      int[] helperColumn = new int[this.currentBoard.length];
      for (int j = 0; j < this.currentBoard.length; j++) {
        helperColumn[j] = this.currentBoard[j][i]; //Column Aggregator
        String boxKey = "Box " + Integer.toString(boxChoose(i+1, j+1, num));

        //Prepping boardState for full box transfer
        boardState.put(boxKey, new int[this.currentBoard.length]);

        //Box aggregation
        if (boxes.get(boxKey) == null) {
          boxes.put(boxKey, new ArrayList<>());
        }
        boxHelper = boxes.get(boxKey);
        boxHelper.add(this.currentBoard[i][j]);
        boxes.put(boxKey,boxHelper); // Box Creator
      }
      boardState.put("Column " + Integer.toString(i+1), helperColumn); // Column Creator
    }

    //Transfer final box list from helper to main boardState
    for (int i = 0; i < this.currentBoard.length; i++) {
      for (String key : boxes.keySet()) {
        boardState.get(key)[i] = boxes.get(key).get(i);
      }
    }
    boardState.forEach((k,v) -> System.out.println(
                    k + " = " + Arrays.toString(boardState.get(k))));
  }
  public static int boxChoose(int row, int column, int num) {
     int rowChunk = ((row-1)/num)+1;
     int columnChunk = ((column - 1)/num)+1;
     int boxNumber = num*(rowChunk-1)+columnChunk;
     return boxNumber;
  }
  public boolean rowUnique (int row, int number) {
      boolean rowUnique = true;
      for (int i : this.getBoardState("Row " + row)) {
          if (i == number) {
              rowUnique = false;
          }
      } return rowUnique;
  }
  public boolean boxUnique (int box, int number) {
      boolean boxUnique = true;
      for (int i : this.getBoardState("Box "+ box)) {
          if (i == number) {
              return false;
          }
      } return boxUnique;
  }
  public boolean columnUnique (int column, int number) {
      boolean columnUnique = true;
      for (int i : this.getBoardState("Column " + column)) {
          if (i == number) {
              return false;
          }
      } return columnUnique;
  }
  public void chooseRow(int row) {
    if (row > 0 && row <= this.startBoard.length) {
      this.setIsRowChosen(true);
    } else if (row == 88) {
      //Undo function activates
    } else if (row == 99) {
      //quit function activates
    } else {
      System.out.println("Please choose a row between 1 and " + this.startBoard.length
       + ", 88 to undo a move, or 99 to quit the current game.");
    }

  }
  public void chooseColumn(int column) {
    if (column > 0 && column <= this.startBoard.length) {
      this.setIsColumnChosen(true);
    } else if (column == 88) {
      //Undo function activates
    } else if (column == 99) {
      //quit function activates
    } else {
      System.out.println("Please choose a column between 1 and " + this.startBoard.length
       + ", 88 to undo a move, or 99 to quit the current game.");
    }
  }
  public void chooseNumber(int number, int row, int column) {
    if (number > 0 && number <= this.startBoard.length) {
      this.setIsNumberChosen(true);
    } else if (number == 88) {
      //Undo function activates
    } else if (number == 99) {
      //quit function activates
    } else {
      System.out.println("Please choose a number between 1 and " + this.startBoard.length
       + ", 88 to undo a move, or 99 to quit the current game.");
    }
  }
  public int[] replaceNumber(int[] arrayHelper, int numHold, int number) {
    for (int i = 0; i < arrayHelper.length; i++) {
      if (arrayHelper[i] == numHold) {
        arrayHelper[i] = number;
        break;
      }
    }
    return arrayHelper;
  }
    //this version of placeNumber assumes valid placement
  public void placeNumber(int row, int column, int number) {
    //Holding the number to check inside the replaceNumber function
    int numHold = this.getCurrentBoardNumber(row,num);
    String lastMove = writeLastMove(row,column, number);
    this.setGameHistory(lastMove);

    //Put the number in the Row Key
    int[] arrayHelper = this.getBoardState("Row " + row);
    arrayHelper = this.replaceNumber(arrayHelper, numHold, number);
    this.setBoardState("Row " + row, arrayHelper);

    //Puts the number in the Column Key
    arrayHelper = this.getBoardState("Column " + column);
    arrayHelper = this.replaceNumber(arrayHelper, numHold, number);
    this.setBoardState("Column " + column, arrayHelper);

    //Puts the number in the Box Key
    arrayHelper = this.getBoardState("Box " + boxChoose(row, column, this.num));
    arrayHelper = this.replaceNumber(arrayHelper, numHold, number);
    this.setBoardState("Box " + boxChoose(row,column,this.num), arrayHelper);


    this.setCurrentBoardNumber(row, column, number);
    this.gameCount++;
  }

  public String writeLastMove(int row, int column, int number) {
    int originalNum = this.getCurrentBoardNumber(row,column);
    String lastMove = "Replaced " + originalNum + " at Row " + row + " Column " + column + " with " + number;
    return lastMove;
  }
}
