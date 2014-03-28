#include "taskmanager.h"

TaskManager::TaskManager(QObject *parent) :
    QObject(parent)
{
    this->updatePlaylist("pl.json");
}

// 1. Проверить, не пора ли обновить плейлист
// 2. Просмотреть последнюю отданую задачу, не закончилась ли она
// 3. Если закончилась, то взять новую задачу из текущего промежутка, при этом обновив состояния элементов, если надо
void TaskManager::update()
{

}

void TaskManager::updatePlaylist(QString filename)
{
    this->play_list.clear();
    QFile file(filename);
    if (!file.open(QFile::ReadOnly))
        return;

    QJsonDocument document = QJsonDocument::fromJson(file.readAll());
    QJsonArray root_array = document.array();
    foreach (const QJsonValue& item, root_array)
    {
        QJsonObject obj = item.toObject();

        QString time_string = obj["time"].toString();
        QJsonArray item_array = obj["action"].toArray();
        QStringList actions;
        foreach (const QJsonValue& action_item, item_array)
        {
            QJsonObject action_obj = action_item.toObject();
            QString action = action_obj["action"].toString();
            QString param = action_obj["params"].toString();
            if (param.length() > 0)
                actions.append(action + QString(" ") + param);
            else
                actions.append(action);
        }

        QTime time = QTime::fromString(time_string, "hh:mm:ss");
        this->play_list[time] = actions;
    }
}
