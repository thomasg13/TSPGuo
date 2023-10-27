import java.io.*;
import java.util.*;
import javax.swing.*;
import java.awt.*;
import javax.swing.*;

public class Driver{
   public static void main(String[] args){
      JFrame frame = new JFrame("Display");
      frame.setSize(800, 800);//chane this
      frame.setResizable(false);
      frame.setLocation(0, 0);
      Board c = new Board();
      frame.setContentPane(c);
      //frame.setLayout(new BorderLayout());
      //frame.add(c, BorderLayout.CENTER);
      frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
      frame.setVisible(true);
      c.start();
   }
}