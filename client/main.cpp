#include "mainwindow.h"
#include <QApplication>

int main(int argc, char *argv[])
{
    QApplication a(argc, argv);
    QApplication::setOrganizationName("allsol");
    QApplication::setApplicationName("videoad");
    MainWindow* w = new MainWindow();
    w->show();
    
    return a.exec();
}
