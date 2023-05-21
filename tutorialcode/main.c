#include "graphics.h"
#include "extgraph.h"

void Main()
{
    SetWindowTitle("DrawHouse");
    InitGraphics();
    
    double w = GetWindowWidth(), h = GetWindowHeight();
    MovePen(w/4,h/5);
    DrawLine(w/4,0);
    DrawLine(0,w/4);
    DrawLine(-w/4,0);
    DrawLine(0,-w/4);
    MovePen(w/4+w/8,h/5);
    DrawLine(0,3*w/16);
    DrawLine(w/16,0);
    DrawLine(0,-3*w/16);
    MovePen(w/4+w/16,h/5+3*w/16);
    DrawLine(w/20,0);
    DrawLine(0,-w/20);
    DrawLine(-w/20,0);
    DrawLine(0,w/20);
    MovePen(w/4,h/5+w/4);
    DrawLine(w/8,w/4);
    DrawLine(w/8,-w/4);
    MovePen(w/4+w/32,h/5+w/4+w/16);
    DrawLine(0,w/8);
    DrawLine(w/32,0);
    DrawLine(0,-w/16);
    MovePen(w/4+w/32-w/128,h/5+w/4+w/16+w/8);
    DrawLine(0,w/64);
    DrawLine(w/32+w/64,0);
    DrawLine(0,-w/64);
    DrawLine(-w/32-w/64,0);
    
}

