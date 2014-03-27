#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QMainWindow>
#include <QTableWidget>
#include <QTextBrowser>
#include <QVBoxLayout>
#include <QHBoxLayout>
#include <QLabel>
#include <QtMultimediaKit/QMediaPlayer>
#include <QGraphicsView>
#include <QSettings>


namespace Ui {
class MainWindow;
}

class MainWindow : public QMainWindow
{
    Q_OBJECT
    
public:
    explicit MainWindow(QWidget *parent = 0);
    ~MainWindow();
    
private:
    void DisplayImage(QGraphicsView* view, QString path);


    Ui::MainWindow *ui;

    QTableWidget* bus_schedule;

    QLabel* news_label_time;
    QLabel* news_label_temperature;
    QTextBrowser* news_text;
    QVBoxLayout* news_box;
    QHBoxLayout* news_with_bus_schedule;

    QGraphicsView* video_view;

    QList<QTextBrowser*> text_advicements;
    QVBoxLayout* text_box;

    QGraphicsView* picture_krasnoyarsk;



};

#endif // MAINWINDOW_H
