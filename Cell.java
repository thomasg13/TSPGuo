import javax.swing.*;
import java.awt.*;
import java.awt.event.*;

public class Cell extends JButton implements MouseListener{
   private int row;
   private int column;
   private boolean activated = false;
   
   public Cell(int r, int c){
      addMouseListener(this);
      row = r;
      column = c;
   }
   
   public boolean getActivated(){
      return activated;
   }
   
   public void activate(int a){
      String s = "" + a;
      this.setText(s);
      activated = true;
   }
   
   public void	mouseClicked(MouseEvent e){}
   public void	mouseEntered(MouseEvent e){}
   public void	mouseExited(MouseEvent e){}
   public void	mousePressed(MouseEvent e){}
   public void	mouseReleased(MouseEvent e){}
}