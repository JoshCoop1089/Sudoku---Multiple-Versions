/**
 * @Author: Josh Cooper
 * @Date:   2018-11-01T12:01:08-04:00
 * @Email:  joshcoop1089@gmail.com
 * @Last modified by:   Josh Cooper
 * @Last modified time: 2018-11-27T19:42:30-05:00
 */
import java.util.*;
public class Tests {
  public static void replaceTester(int row, int column, int number, int box, Board current) {
    System.out.println("\nTesting Number placement/replacing");
    System.out.println("\nRow " + row + " was: \t" +
                  Arrays.toString(current.getBoardState("Row " + row)));
    System.out.println("Column " + column + " was: \t" +
                  Arrays.toString(current.getBoardState("Column " + column)));
    System.out.println("Box " + box + " was: \t" +
                  Arrays.toString(current.getBoardState("Box " + box)));
    System.out.println("\nPutting " + number + " at Row " + row + " Column " + column);

    current.placeNumber(row,column,number);

    System.out.println("\nRow " + row + " is now: \t" +
                  Arrays.toString(current.getBoardState("Row " + row)));
    System.out.println("Column " + column + " is now:" +
                  Arrays.toString(current.getBoardState("Column " + column)));
    System.out.println("Box " + box + " is now: \t" +
                  Arrays.toString(current.getBoardState("Box " + box))+ "\n");
  }
  public static void main(String[] args) {

    Board small = Board.boardStart();
    if (small != null) {
      small.startBoardState();
      System.out.println(small.getBoardFileName());
      small.boardPrint();
      for (int i = 1; i < 4; i++) {
        int row = i;
        int column = i;
        int number = 2*i;
        int box = Board.boxChoose(row, column, small.getNum());
        replaceTester(row,column,number,box,small);
        small.boardPrint();
      }

      System.out.println(small.getGameHistory(1));
      System.out.println(small.getGameHistory(2));
      System.out.println(small.getGameHistory(3));
    }
  }
}
