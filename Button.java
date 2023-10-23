import java.awt.*;
import javax.swing.JButton;

public class Button extends JButton{
    private Shape shape;
    private String title;
    private Color color;
    private Color regularColor;
    private Color highlightColor;
    private Color textColor;
    
    public Button(Shape s, String t, Color rc, Color hc, Color tc){
        shape = s;
        title = t;
        regularColor = rc;
        highlightColor = hc;
        textColor = tc;
        color = regularColor;
    }

    //GETTERS
    public Shape getShape(){
        return shape;
    }

    public String getTitle(){
        return title;
    }

    public Color getColor() {
        return color;
    }

    public Color getRegularColor() {
        return regularColor;
    }

    public Color getHighlightColor() {
        return highlightColor;
    }

    public Color getTextColor() {
        return textColor;
    }

    //SETTERS
    public void setShape(Shape shape){
        this.shape = shape;
    }

    public void setTitle(String title){
        this.title = title;
    }

    public void setColor(Color color) {
        this.color = color;
    }

    public void setRegularColor(Color regularColor) {
        this.regularColor = regularColor;
    }

    public void setHighlightColor(Color highlightColor) {
        this.highlightColor = highlightColor;
    }

    public void setTextColor(Color textColor) {
        this.textColor = textColor;
    }
    //

    public void highlight(){
        color = highlightColor;
    }

    public void unHighlight(){
        color = regularColor;
    }

    @Override
    protected void paintComponent(Graphics g){
        super.paintComponent(g);
        drawButton(g);
    }

    public void drawButton(Graphics g){
        int x = (int)(this.getShape().getBounds().getX());
        int y = (int)(this.getShape().getBounds().getY());
        int width = (int)(this.getShape().getBounds().getWidth());
        int height = (int)(this.getShape().getBounds().getHeight());
        g.setColor(this.getColor());
        g.fillRect(x, y, width, height);
        g.setColor(this.getTextColor());
        g.drawString(this.getTitle(), x + (width/3), y + (height/2 + 5));
    }

}
