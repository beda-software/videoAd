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
#include <QTime>

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

    void setBus(QMap<int, QString> buses);
    void setNews(QString news_text);

    void updateLabels(QString temperature);

    explicit MainWindow(QWidget *parent = 0);
    ~MainWindow();

signals:
    void video_finished();

private slots:
    void player_state_changed(QMediaPlayer::State);
    
private:
    void displayImage(QGraphicsView* view, QString path);

    QTableWidget* bus_schedule;

    QLabel* news_label_time;
    QLabel* news_label_temperature;
    QTextBrowser* news_text;

    QGraphicsView* video_view;
    QMediaPlayer* video_player;
    QGraphicsVideoItem* video_item;

    int current_advicement_index;
    QList<QTextBrowser*> text_advicements;

    QGraphicsView* picture_krasnoyarsk;
};

#endif // MAINWINDOW_H
