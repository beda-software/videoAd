#include "mainwindow.h"
#include "taskmanager.h"
#include <QApplication>

int main(int argc, char *argv[])
{
    QApplication a(argc, argv);
    MainWindow* w = new MainWindow();
    TaskManager* task_manager = new TaskManager(w);
    w->show();
    
    return a.exec();
}
