import java.awt.*;
import javax.swing.*;
import java.io.*;
import java.util.*;

public class Board extends JPanel{
   private static final int DIM = 20;
   private static Cell[][] cells = new Cell[DIM][DIM];
   private static int x1, x2, x3, x4, x5, y1, y2, y3, y4, y5;
   public static int[][] path = new int[DIM][2];//x, y
   public static double[][] distances = new double[DIM][DIM];
   public static int[] order = new int[DIM];
   public static boolean useSingle;
   public static int[][] pairs = new int[DIM][2];//change size for now
   
   public Board(){
      setLayout(new GridLayout(DIM, DIM));
      for (int r = 0; r < cells.length; r++){
         for (int c = 0; c < cells[0].length; c++){
            cells[r][c] = new Cell(r, c);
            add(cells[r][c]);
            cells[r][c].setBackground(new Color(70, 240, 110)); // (70, 240, 110) for a good green
            cells[r][c].setEnabled(false);
         }
      }
      useSingle = true;
   }
   
   public static void start(){
      int places = 20;//change this
      int edges = 8;
      int indexes[][] = new int[places][2];
      for(int i = 0; i < places; i ++){
         int a = (int)(Math.random() * DIM);
         int b = (int)(Math.random() * DIM);
         if(!cells[a][b].getActivated()){
            cells[a][b].activate(i + 1);
            cells[a][b].setBackground(Color.WHITE);
            /*if(i == 0){
               cells[a][b].setBackground(Color.GREEN);
            }
            if(i == places - 1){
               cells[a][b].setBackground(Color.RED);
            }*/
            indexes[i][0] = cells[a][b].getX() + 25;
            indexes[i][1] = cells[a][b].getY() + 25;         
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
      /*for (int r = 0; r < cells.length; r++){
         for (int c = 0; c < cells[0].length; c++){
            if(!cells[r][c].getActivated()){
               cells[r][c].deactivate();
            }
         }
      }*/
      for(int i = 0; i < DIM; i ++){
         Cell a = find(i + 1);
         for(int j = 0; j < DIM; j ++){
            Cell b = find(j + 1);
            int ax = a.getColumn();
            int bx = b.getColumn();
            int ay = a.getRow();
            int by = b.getRow();
            int length = Math.abs(ax - bx);
            int width = Math.abs(ay - by);
            double distance = Math.sqrt((int)Math.pow(length, 2) + (int)Math.pow(width, 2));
            distances[i][j] = distance;
         }
      }
      //nearestAvailableNeighbor();
      greedy();
   }

   
   public static Cell find(int n){
      for(int r = 0; r < DIM; r ++){
         for(int c = 0; c < DIM; c ++){
            if(cells[r][c].getNumber() == n){
               return cells[r][c];
            }
         }
      }
      return null;
   }
   
   public static void nearestAvailableNeighbor(){
      boolean[] used = new boolean[DIM];
      for(int i = 0; i < DIM; i ++){
         used[i] = false;
      }
      used[0] = true;
      int count = 0;
      int current = 0;
      //Cell c = find(current )
      boolean ongoing = true;
      while(ongoing){
         double lowest = 100;
         int lowestIndex = -1;
         for(int i = 0; i < DIM; i ++){
            if(!used[i] && distances[current][i] < lowest){
               lowestIndex = i;
               lowest = distances[current][i];
            }
         }
         if(lowestIndex == -1){
            break;//in theory, means there are none left
         }
         used[lowestIndex] = true;
         order[count + 1] = lowestIndex;
         count++;
         current = lowestIndex;
      }
      
   }
   
   public static void greedy(){
      useSingle = false;
      int[] used = new int[DIM];
      for(int i = 0; i < DIM; i ++){
         used[i] = 0;
      }
      boolean ongoing = true;
      int count = 0;
      while(ongoing){
         double currentMin = 100;
         double tempMax = 0;//helps solve problems
         int currentI = -1;
         int currentJ = -1;
         for(int i = 0; i < DIM; i ++){
            for(int j = 0; j < DIM; j ++){
               boolean works = true;
               if((distances[i][j] < currentMin) && used[i] < 2 && used[j] < 2 && i != j){//make sure its not duplicate but reverse
                  boolean alreadyDone = false;
                  for(int k = 0; k < DIM; k ++){
                     if( (pairs[k][0] == j && pairs[k][1] == i) || (pairs[k][0] == i && pairs[k][1] == j)){
                        works = false;
                     }
                    
                  }
               }else{
                  works = false;
               }
               //check for cycles
               /*
               if(used[i] == 1 && used[j] == 1){
                  int index = i;
                  int indexInPairs = -1;
                  while(true){
                     for(int m = 0; m < DIM; m ++){
                        if(pairs[m][0] == index){
                           index = pairs[m][1];
                           break;
                        }else if(pairs[m][1] == index){
                           index = pairs[m][0];
                           break;
                        }
                     }
                     if(index == j){
                        works = false;
                        break;
                     }else{
                        if(!(used[index] == 2)){
                           break;
                        }
                     }
                  }
               }*/
               
               
               if(works){
                  currentMin = distances[i][j];
                  currentI = i;
                  currentJ = j;
                     
               }
            }
         }
         if(currentI == -1){
            ongoing = false;
            break;
         }else{//add the pair
            pairs[count][0] = currentI;
            pairs[count][1] = currentJ;
            used[currentI] = used[currentI] + 1;
            used[currentJ] = used[currentJ] + 1;
            count ++;
         }
      }
   }
   
   public static int findBestPath(ArrayList<Integer> a){
      return 0;
   }
   
   public static void bruteForce(){
      int[] arr = new int [DIM];
      ArrayList<Integer> a = new ArrayList<Integer>();
      findBestPath(a);
   }
   
   
   @Override 
   public void paint(Graphics g) {
      super.paint(g);
      Graphics2D g2 = (Graphics2D) g;
      g2.setStroke(new BasicStroke(3));
      /*
      g.drawLine(x1, y1, x2, y2);
      g.drawLine(x2, y2, x3, y3);
      g.drawLine(x3, y3, x4, y4);
      g.drawLine(x4, y4, x5, y5);
      g.drawLine(x5, y5, x1, y1);
      */
      if(useSingle){
         int ax = 0;
         int ay = 0;
         int bx = 0;
         int by = 0;
      
         Cell a = find(order[0] + 1);
         int ax1 = a.getX() + 25;
         int ay1 = a.getY() + 25;
         for(int i = 1; i < DIM; i ++){
            Cell b = find(order[i] + 1);
            ax = a.getX() + 25;
            ay = a.getY() + 25;
            bx = b.getX() + 25;
            by = b.getY() + 25;
            g.drawLine(ax, ay, bx, by);
            a = find(order[i] + 1);
         }
         g.drawLine(ax1, ay1, bx, by);
      }else{
         for(int i = 0; i < DIM; i ++){
            int ax = 0;
            int ay = 0;
            int bx = 0;
            int by = 0;
            Cell a = find(pairs[i][0] + 1);
            Cell b = find(pairs[i][1] + 1);
            ax = a.getX() + 25;
            ay = a.getY() + 25;
            bx = b.getX() + 25;
            by = b.getY() + 25;
            g.drawLine(ax, ay, bx, by);
         }
      }
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