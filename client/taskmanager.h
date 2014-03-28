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

#include <QDebug>


#define IMAGE_DURATION 10
#define TEXT_DURATION 10


class TaskManager : public QObject
{
    Q_OBJECT
public:
    explicit TaskManager(QObject *parent = 0);
    
signals:
    
public slots:
    void update();

private:
    void updatePlaylist(QString filename);

    QTime task_finish_time;
    QMap<QTime, QStringList> play_list;
    
};

#endif // TASKMANAGER_H
