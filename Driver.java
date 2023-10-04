import java.io.*;
import java.util.*;
import javax.swing.*;
import java.awt.*;

public class Driver{
   public static void main(String[] args){
      JFrame frame = new JFrame("Display");
      Board c = new Board();
      frame.setSize(1000, 1000);
      frame.setResizable(false);
      frame.setLocation(0, 0);
      frame.setContentPane(c);
      frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
      frame.setVisible(true);
      //frame.getContentPane().add(b, BorderLayout.EAST);
      c.start();
   }
}