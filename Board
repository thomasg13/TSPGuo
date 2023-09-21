import java.awt.*;
import javax.swing.*;

public class Board extends JPanel{
   private static final int DIM = 20;
   private static Cell[][] cells = new Cell[DIM][DIM];
   private static int x1, x2, x3, x4, x5, y1, y2, y3, y4, y5;
   
   public Board(){
      setLayout(new GridLayout(DIM, DIM));
      for (int r = 0; r < cells.length; r++){
         for (int c = 0; c < cells[0].length; c++){
            cells[r][c] = new Cell(r, c);
            add(cells[r][c]);
            //cells[r][c].setBackground(Color.YELLOW);
         }
      }
   }
   
   public static void start(){
      int places = 5;//change this
      int edges = 8;
      int indexes[][] = new int[5][2];
      for(int i = 0; i < places; i ++){
         int a = (int)(Math.random() * DIM);
         int b = (int)(Math.random() * DIM);
         if(!cells[a][b].getActivated()){
            cells[a][b].activate(i + 1);
            cells[a][b].setBackground(Color.WHITE);
            indexes[i][1] = a * 50;
            indexes[i][0] = b * 50;
         }else{
            i --;
         }
      } 
      x1 = indexes[0][0];
      y1 = indexes[0][1];
      x2 = indexes[1][0];
      y2 = indexes[1][1];
      x3 = indexes[2][0];
      y3 = indexes[2][1];
      x4 = indexes[3][0];
      y4 = indexes[3][1];
      x5 = indexes[4][0];
      y5 = indexes[4][1];
      for (int r = 0; r < cells.length; r++){
         for (int c = 0; c < cells[0].length; c++){
            if(!cells[r][c].getActivated()){
               cells[r][c].deactivate();
            }
            
         }
      }
      for(int i = 0; i < 7; i ++){

      }
   }
   
   
   
   @Override 
   public void paint(Graphics g) {
      super.paint(g);
      g.drawLine(x1, y1, x2, y2);
      g.drawLine(x2, y2, x3, y3);
      g.drawLine(x3, y3, x4, y4);
      g.drawLine(x4, y4, x5, y5);
      g.drawLine(x5, y5, x1, y1);
   }
   
   public static void main(String[] args){
      JFrame frame = new JFrame("Graph");
      frame.setSize(1000, 1000);
      frame.setLocation(0, 0);
      frame.setContentPane(new Board());
      frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
      frame.setVisible(true);
      start();
   }
}
