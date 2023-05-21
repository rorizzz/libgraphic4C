#include "graphics.h"
#include "extgraph.h"
#include "genlib.h"
#include "simpio.h"
//#include "conio.h"
#include <stdio.h>
//#include <stdlib.h>
//#include <stddef.h>
 
#include <windows.h>
//#include <olectl.h>
//#include <stdio.h>
//#include <mmsystem.h>
//#include <wingdi.h>
//#include <ole2.h>
//#include <ocidl.h>
#include <winuser.h>
 
int cx,cy;
 
bool inBox(double x0, double y0) //check if the pen is in the graph window
{
	return (x0 > 0 && x0 < cx && y0 > 0 && y0 < cy);
}
 
void MouseEventProcess(int x, int y, int button, int event)
{ 
	static double lx=0.0, ly=0.0;
    double mx, my;
 	 mx = ScaleXInches(x); //pixels for every inches
 	 my = ScaleYInches(y);
 	 static bool isDraw = FALSE;
 
     switch (event) {
         case BUTTON_DOWN:
   		 	  if (button == LEFT_BUTTON){ //when press the mouse left button, set the isDraw True
				  isDraw = TRUE;	
   		 	} 
              break;
    	 case BUTTON_DOUBLECLICK:
			  break;
         case BUTTON_UP: //if lift it up,stop drawing
  		 	  if (button == LEFT_BUTTON) isDraw = FALSE;
              break;
         case MOUSEMOVE:
			  if (isDraw) {
			  	  DrawLine(mx-lx,my-ly);
			  	  MovePen(mx,my);
			  } 
              break;
     }	
     lx=mx;
     ly=my;
}
 
 
void Main()
{
    InitGraphics();        	
	cx = GetWindowWidth();
    cy = GetWindowHeight();
	registerMouseEvent(MouseEventProcess);
    SetPenSize(2); //set the pensize
}
