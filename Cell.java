import javax.swing.*;
import java.awt.*;
import java.awt.event.*;

public class Cell extends JButton implements MouseListener{
   private int row;
   private int column;
   private boolean activated = false;
   private int value;
   
   public Cell(int r, int c){
      addMouseListener(this);
      row = r;
      column = c;
      value = -1;
   }
   
   public boolean getActivated(){
      return activated;
   }
   
   public int getRow(){
      return row;
   }
   
   public int getColumn(){
      return column;
   }
   
   public int getNumber(){
      return value;
   }
   
   public void activate(int a){
      String s = "" + a;
      this.setText(s);
      value = a;
      activated = true;
      this.setEnabled(false);
   }
   
   public void deactivate(){
      this.setOpaque(true);
      this.setContentAreaFilled(false);
      this.setBorderPainted(false);
      activated = false;
   }
   
   public void	mouseClicked(MouseEvent e){}
   public void	mouseEntered(MouseEvent e){}
   public void	mouseExited(MouseEvent e){}
   public void	mousePressed(MouseEvent e){}
   public void	mouseReleased(MouseEvent e){}
}
