#include <GL/freeglut.h>
#include <iostream>
#include <math.h>

void init(void){
    glClearColor(0.0, 0.0, 0.0, 1.0);
    glMatrixMode(GL_PROJECTION);
    gluOrtho2D(0.0, 300.0, 0.0, 200.0);
}

void lineBresenhams(int  x0, int y0, int xend, int yend) {
  int dx = abs(xend - x0);
  int dy = abs(yend - y0);
  int x = x0;
  int y = y0;
  int i,p;

  glBegin(GL_LINE_STRIP);
    glVertex2i(x, y);
  if (dy < dx) {
  	p = 2 * dy - dx;
    for (i = 1; i <= dx; i++) {
      if (p < 0) {
        p = p + 2 * dy;
      } else {
        p = p + 2 * dy - 2 * dx;
        y++;
      }
      x++;
      glVertex2i(x, y);
    }
  } else {
  	p = 2 * dx - dy;
    for (i = 1; i <= dy; i++) {
      if (p < 0) {
        p = p + 2 * dx;
      } else {
        p = p + 2 * dx - 2 * dy;
        x++;
      }
      y++;
      glVertex2i(x, y);
    }
  }
    glEnd();
    glFlush();
}
void display() {
    glClear(GL_COLOR_BUFFER_BIT);
    glColor3f(1.0, 1.0, 1.0); // Set line color to yellow
    
    // Draw a sample line from (150, 50) to (150, 250)
    lineBresenhams(50,100,75,150);
}
int main(int argc, char** argv) {
    glutInit(&argc, argv);
    glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB);
    glutInitWindowSize(500, 500);
    glutCreateWindow("Bresenham's Line Algorithm");
    init();
    glutDisplayFunc(display);
    glutMainLoop();
    return 0;
}