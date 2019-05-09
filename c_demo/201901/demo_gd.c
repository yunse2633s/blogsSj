#define GLUT_BUILDING_LIB
#define GLUT_DISABLE_ATEXIT_HACK
#include <gl/freeglut.h>
// 不能使用，安装了freeglut
int main(int argc, char** argv){
  glutInit(&argc, argv);
  glutInitWindowSize(200, 200);
  glutCreateWindow("WindowTitle");
  glutMainLoop();

  return 0;
}