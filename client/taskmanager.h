#ifndef TASKMANAGER_H
#define TASKMANAGER_H

#include <QObject>
#include <QTime>
#include <QMap>
#include <QJsonDocument>
#include <QJsonArray>
#include <QJsonObject>
#include <QString>
#include <QStringList>
#include <QFile>
#include <QDir>
#include <QTimer>
#include <QSettings>

#include <QDebug>

#include "mainwindow.h"
#include "contentloader.h"


#define IMAGE_DURATION 30
#define TEXT_DURATION 8
#define DAYS_BACK_MAX 5


struct Contents
{
    QString type;
    QString param;
};


class TaskManager : public QObject
{
    Q_OBJECT
public:
    explicit TaskManager(MainWindow* window, ContentLoader* loader, QObject *parent = 0);
    
signals:
    
public slots:
    void update();

    void video_finished();
    void text_finished();

    void load_bus();
    void load_news();

private slots:
    void getCurrentTasks();


private:
    void updatePlaylist();
    void updateTasksList();
    void updatePlaylistFromFile(QString filename);

    QTime getNextTaskTime();


    int current_video_index;
    QStringList current_videos;

    int current_text_index;
    QStringList current_texts;

    QTime current_played_time;
    QDir* current_directory;
    QMap<QTime, QList<Contents> > play_list;

    QTimer* image_finish_timer;
    QTimer* text_finish_timer;
    QTimer* update_timer;
    MainWindow* main_window;


    ContentLoader* content_loader;
    QTimer* load_bus_timer;
    QTimer* load_news_timer;
};

#endif // TASKMANAGER_H
