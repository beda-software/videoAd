#include "mainwindow.h"
#include "taskmanager.h"
#include "contentloader.h"
#include <QApplication>

int main(int argc, char *argv[])
{
    QApplication a(argc, argv);
    ContentLoader* loader = new ContentLoader();
    MainWindow* w = new MainWindow();
    TaskManager* task_manager = new TaskManager(w, loader);
    w->show();
    
    return a.exec();
}
