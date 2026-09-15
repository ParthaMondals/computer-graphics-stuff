#include <GL/freeglut.h>
#include <iostream>
#include <math.h>
int r,xc,yc;
void init(void){
    glClearColor(0.0, 0.0, 0.0, 1.0);
    glMatrixMode(GL_PROJECTION);
    gluOrtho2D(0.0, 500.0, 0.0, 300.0);
}

void setPixel(int x, int y){
    int ncx,ncy;
    ncx = xc + 150;
    ncy = yc + 150;
    glBegin(GL_POINTS);
        glVertex2i(x + ncx, y + ncy);
    glEnd();
    glFlush();
}

void midpoint_circle(int r){
	int x,y,p;
	x = 0;
    y = r;
	p = 1 - r;
	
	while(x <= y){		
        setPixel(x,y);
        setPixel(y,x);
        setPixel(-x,y);
        setPixel(-y,x);
        setPixel(-x,-y);
        setPixel(-y,-x);
        setPixel(x,-y);
        setPixel(y,-x);          
		x++;
		if(p > 0){
			y = y - 1;
			p = p + (2*x) - (2*y) + 1;
		}
		else{
            p = p + (2*x) + 1;
        }
	}
}

void display(){
    glClear(GL_COLOR_BUFFER_BIT);
    glColor3f(1.0, 1.0, 1.0); // Set line color to yellow
    
    // Draw a sample line from (150, 50) to (150, 250)
    midpoint_circle(r);
}
int main(int argc, char** argv) {
	printf("Enter the radius: ");
	scanf("%d",&r);
	printf("Enter the x coordinate of center: ");
	scanf("%d",&xc);
	printf("Enter the y coordinate of center: ");
	scanf("%d",&yc);

    glutInit(&argc, argv);
    glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB);
    glutInitWindowSize(500, 500);
    glutCreateWindow("Midpoint Circle drawing Algorithm");
    init();
    glutDisplayFunc(display);
    glutMainLoop();
    return 0;
}