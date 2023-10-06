import java.io.*;
import java.util.*;
import javax.swing.*;
import java.awt.*;
import javax.swing.*;

public class Driver{
   public static void main(String[] args){
      JFrame frame = new JFrame("Display");
      Board c = new Board();
      Yo y = new Yo();
      frame.setSize(2000, 1000);
      frame.setResizable(false);
      frame.setLocation(0, 0);
      frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
      frame.setVisible(true);
      frame.setLayout(new BorderLayout());
      frame.add(c, BorderLayout.WEST);
      frame.add(y, BorderLayout.CENTER);
      //frame.getContentPane().add(b, BorderLayout.EAST);
      c.start();
      y.start();
      //SwingUtilities.invokeLater(() -> new FrameWithTwoPanels());
   }
}