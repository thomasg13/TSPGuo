import java.awt.*;
import javax.swing.*;

public class Yo extends JPanel{
   private static final int DIM = 20;
   private static Cell[][] cells = new Cell[DIM][DIM];
   private static int x1, x2, x3, x4, x5, y1, y2, y3, y4, y5;
   
   private static Button[] buttons = new Button[12];
   private static Shape r1 = new Rectangle(10, 10, 130, 55);
   
   public void buttonSetup(){
        buttons[0] = new Button(r1, "Brute Force", Color.YELLOW, Color.decode("#B67949"), Color.BLACK);
   }
   
   public Yo(){
      buttonSetup();
   }      
   
   @Override 
   public void paint(Graphics g) {
      super.paint(g);
      Graphics2D g2 = (Graphics2D) g;
      buttons[0].drawButton(g);
   }
 
   /*  
   public static void main(String[] args){
      JFrame frame = new JFrame("Graph");
      frame.setSize(1000, 1000);
      frame.setResizable(false);
      frame.setLocation(0, 0);
      frame.setContentPane(new Board());
      frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
      frame.setVisible(true);
      start();
   }*/
}