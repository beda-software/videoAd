#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QMainWindow>
#include <QTableWidget>
#include <QTextEdit>
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
    Ui::MainWindow *ui;

    QTableWidget* bus_schedule;

    QLabel* news_label_time;
    QLabel* news_label_temperature;
    QTextEdit* news_text;
    QVBoxLayout* news_box;

    QGraphicsView* video_view;

    QList<QTextEdit*> text_advicements;
    QVBoxLayout* text_box;



};

#endif // MAINWINDOW_H
