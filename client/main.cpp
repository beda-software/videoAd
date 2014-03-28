#include "mainwindow.h"
#include "taskmanager.h"
#include <QApplication>

int main(int argc, char *argv[])
{
    QApplication a(argc, argv);
    TaskManager task_manager;
    MainWindow w;
    w.show();
    
    return a.exec();
}
