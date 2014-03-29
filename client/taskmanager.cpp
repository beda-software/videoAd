#include "taskmanager.h"

TaskManager::TaskManager(MainWindow *window, ContentLoader *loader, QObject *parent) :
    QObject(parent)
{
    QSettings settings;
    QString work_dir = settings.value("work_dir", "/tmp/").toString();
    this->current_directory = new QDir(work_dir);

    this->updatePlaylist();
    this->current_played_time = QTime::currentTime();
    this->current_text_index = this->current_video_index = 0;
    this->main_window = window;
    this->content_loader = loader;

    this->image_finish_timer = new QTimer();
    connect(this->image_finish_timer, SIGNAL(timeout()), this, SLOT(video_finished()));
    this->text_finish_timer = new QTimer();
    connect(this->text_finish_timer, SIGNAL(timeout()), this, SLOT(text_finished()));

    connect(this->main_window, SIGNAL(video_finished()), this, SLOT(video_finished()));

    this->update_timer = new QTimer();
    connect(this->update_timer, SIGNAL(timeout()), this, SLOT(update()));
    this->update_timer->start(1000);

    this->load_bus_timer = new QTimer();
    connect(this->load_bus_timer, SIGNAL(timeout()), this, SLOT(load_bus()));
    this->load_bus_timer->start(5 * 1000);
}

void TaskManager::update()
{
    // не пора ли обновить текущую задачу на воспроизведение
    QTime next_task = this->getNextTaskTime();
    if (!next_task.isNull() && QTime::currentTime() > next_task)
        this->updateTasksList();
}

void TaskManager::video_finished()
{
    qDebug() << "finished";
    this->image_finish_timer->stop();

    if (this->current_videos.length() == 0)
        return;

    QString video = this->current_videos[this->current_video_index];
    bool is_video = false;
    if (video.indexOf(".mp4") > 0 || video.indexOf(".avi") > 0)
        is_video = true;

    this->current_video_index = (this->current_video_index + 1) % this->current_videos.length();
    QString full_path = this->current_directory->absoluteFilePath(video);
    if (is_video)
    {
        this->main_window->displayVideo(full_path);
    }
    else
    {
        this->main_window->displayImage(full_path);
        this->image_finish_timer->start(IMAGE_DURATION * 1000);
    }
}

void TaskManager::text_finished()
{
    this->text_finish_timer->stop();
    if (this->current_texts.length() == 0)
        return;

    QString text = this->current_texts[this->current_text_index];
    this->current_text_index = (this->current_text_index + 1) % this->current_texts.length();
    this->main_window->displayNextAdvicement(text);
    this->text_finish_timer->start(TEXT_DURATION * 1000);
}

void TaskManager::updateTasksList()
{
    this->current_text_index = this->current_video_index = 0;
    this->current_texts.clear();
    this->current_videos.clear();
    this->main_window->stopAll();

    QTime next_task = this->getNextTaskTime();
    QList<Contents> contents = this->play_list[next_task];
    this->current_played_time = next_task;
    foreach (Contents content, contents)
        if (content.type == "video")
            this->current_videos.append(content.param);
        else
            this->current_texts.append(content.param);

    qDebug() << this->current_videos;
    qDebug() << this->current_texts;

    this->text_finished();
    this->video_finished();
}


QTime TaskManager::getNextTaskTime()
{
    QList<QTime> times = this->play_list.keys();
    int minsecs = 80000;
    QTime result;
    foreach (QTime time, times)
    {
        int secs_to = this->current_played_time.secsTo(time);
        if (0 < secs_to && secs_to < minsecs)
        {
            minsecs = secs_to;
            result = time;
        }
    }

    return result;
}


void TaskManager::updatePlaylist()
{
    QDate cur = QDate::currentDate();
    bool finded = false;
    for (int i = 0; i < DAYS_BACK_MAX; i++)
    {
        QString dir_name = cur.toString("dd.MM.yyyy");
        if (this->current_directory->cd(dir_name))
        {
            finded = true;
            break;
        }
        else
        {
            cur = cur.addDays(-1);
        }
    }

    if (!finded)
        return;

    this->updatePlaylistFromFile(this->current_directory->absoluteFilePath("playlist.json"));
}


void TaskManager::updatePlaylistFromFile(QString filename)
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
        QJsonArray item_array = obj["params"].toArray();
        QList<Contents> contents;
        foreach (const QJsonValue& param_item, item_array)
        {
            QJsonObject param_obj = param_item.toObject();
            Contents object;
            object.type = param_obj.keys()[0];
            object.param = param_obj[object.type].toString();

            contents.append(object);
        }

        QTime time = QTime::fromString(time_string, "hh:mm:ss");
        this->play_list[time] = contents;
    }
}

void TaskManager::load_bus()
{
    this->load_bus_timer->stop();
    this->main_window->setBus(this->content_loader->LoadBus());
    this->load_bus_timer->start();
}

void TaskManager::load_news()
{

}
