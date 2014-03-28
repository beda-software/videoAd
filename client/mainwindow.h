#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QMainWindow>
#include <QTableWidget>
#include <QTextBrowser>
#include <QVBoxLayout>
#include <QHBoxLayout>
#include <QLabel>
#include <QMediaPlayer>
#include <QSettings>
#include <QGraphicsItem>
#include <QGraphicsView>
#include <QGraphicsVideoItem>
#include <QGraphicsPixmapItem>


namespace Ui {
class MainWindow;
}

class MainWindow : public QMainWindow
{
    Q_OBJECT
    
public:
    void stopAll();
    void displayNextAdvicement(QString text);
    void displayVideo(QString path);
    void displayImage(QString path);

    explicit MainWindow(QWidget *parent = 0);
    ~MainWindow();

signals:
    void video_finished();

private slots:
    void player_state_changed(QMediaPlayer::State);
    
private:
    void displayImage(QGraphicsView* view, QString path);



    Ui::MainWindow *ui;

    QTableWidget* bus_schedule;

    QLabel* news_label_time;
    QLabel* news_label_temperature;
    QTextBrowser* news_text;
    QVBoxLayout* news_box;
    QHBoxLayout* news_with_bus_schedule;

    QGraphicsView* video_view;
    QMediaPlayer* video_player;
    QGraphicsVideoItem* video_item;
    QGraphicsPixmapItem* pixmap_item;

    int current_advicement_index;
    QList<QTextBrowser*> text_advicements;
    QVBoxLayout* text_box;

    QGraphicsView* picture_krasnoyarsk;



};

#endif // MAINWINDOW_H
