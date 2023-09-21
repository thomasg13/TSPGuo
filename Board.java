import java.awt.*;
import javax.swing.*;

public class Board extends JPanel{
   private static final int DIM = 20;
   private static Cell[][] cells = new Cell[DIM][DIM];
   
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
      for(int i = 0; i < places; i ++){
         int a = (int)(Math.random() * DIM);
         int b = (int)(Math.random() * DIM);
         if(!cells[a][b].getActivated()){
            cells[a][b].activate(i + 1);
            cells[a][b].setBackground(Color.WHITE);
         }else{
            i --;
         }
      } 
      for(int i = 0; i < 7; i ++){
      
      }
   }
   
   
   /*
   @Override 
   public void paint(Graphics g) {
      super.paint(g);
      g.drawLine(100, 100, 200, 200);
      g.drawLine(200, 300 , 300, 300);
   }*/
   
   public static void main(String[] args){
      JFrame frame = new JFrame("Graph");
      frame.setSize(1000,1000);
      frame.setLocation(0, 0);
      frame.setContentPane(new Board());
      frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
      frame.setVisible(true);
   
      start();
   }
}