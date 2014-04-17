#include "mainwindow.h"
#include "ui_mainwindow.h"
#include "tableitemdelegate.h"
#include "taskmanager.h"
#include "contentloader.h"

#include <QDebug>
#include <QTimer>
#include <QApplication>

MainWindow::MainWindow(QWidget *parent) :
    QMainWindow(parent)
{
    if (this->isNight() == MainWindow::NIGHT) {
        float scale = settings.value("scale", 10.0).toFloat();
        bool vertical = settings.value("vertical", true).toBool();
        this->showFullScreen();
        if (vertical) this->setFixedSize(6244/scale, 10969/scale);
        this->setStyleSheet("QMainWindow {background: black;}");
    }
    else {

        float scale = settings.value("scale", 10.0).toFloat();

        this->bus_schedule = new QTableWidget(1, 2, this);
        this->bus_schedule->horizontalHeader()->sectionResizeMode(QHeaderView::Fixed);
        this->bus_schedule->setFrameStyle(QFrame::NoFrame);
        this->bus_schedule->setStyleSheet(""\
                                          "QTableWidget{" \
                                            "gridline-color:black;"\
                                            "background-color:#DCDAD5;"\
                                          "}");
        this->bus_schedule->setVerticalScrollBarPolicy(Qt::ScrollBarAlwaysOff);
        this->bus_schedule->setHorizontalScrollBarPolicy(Qt::ScrollBarAlwaysOff);
        this->bus_schedule->verticalHeader()->hide();
        this->bus_schedule->horizontalHeader()->hide();

        this->news_label_temperature = new QLabel("--------", this);
        QFont label_font = this->news_label_temperature->font();
        label_font.setBold(true);
        label_font.setPointSize((int)600/scale); // TODO setPixelSize
        this->news_label_temperature->setAlignment(Qt::AlignCenter);
        this->news_label_temperature->setFont(label_font);

        this->news_label_time = new QLabel("--------", this);
        this->news_label_time->setAlignment(Qt::AlignCenter);
        this->news_label_time->setFont(label_font);

        this->news_text = new QTextBrowser(this);
        this->news_text->setFrameStyle(QFrame::NoFrame);
        this->news_text->viewport()->setAutoFillBackground(false);
        QFont f = this->news_text->font();
        f.setPointSize((int)150/scale);
        this->news_text->setFont(f);

        this->picture_krasnoyarsk = new QGraphicsView(this);
        this->picture_krasnoyarsk->setVerticalScrollBarPolicy(Qt::ScrollBarAlwaysOff);
        this->picture_krasnoyarsk->setHorizontalScrollBarPolicy(Qt::ScrollBarAlwaysOff);
        QGraphicsScene *picture_scene = new QGraphicsScene(this->picture_krasnoyarsk);
        this->picture_krasnoyarsk->setScene(picture_scene);

        QPixmap pixmap = QPixmap(":/images/krasnoyarsk.jpg");
        QGraphicsPixmapItem* item = new QGraphicsPixmapItem(pixmap.scaled(800/scale,1000/scale));
        picture_scene->addItem(item);
        this->picture_krasnoyarsk->setMaximumSize(800/scale, 1000/scale);
        this->picture_krasnoyarsk->setFrameStyle(QFrame::NoFrame);
        this->picture_krasnoyarsk->viewport()->setAutoFillBackground(false);

        this->video_view = new QGraphicsView(this);
        QGraphicsScene* scene = new QGraphicsScene;
        this->video_view->setScene(scene);
        this->video_view->setHorizontalScrollBarPolicy(Qt::ScrollBarAlwaysOff);
        this->video_view->setVerticalScrollBarPolicy(Qt::ScrollBarAlwaysOff);
        this->video_view->setFrameStyle(QFrame::NoFrame);
        this->video_view->viewport()->setAutoFillBackground(false);

        this->video_player = new QMediaPlayer(this);
        connect(this->video_player, SIGNAL(stateChanged(QMediaPlayer::State)), this, SLOT(player_state_changed(QMediaPlayer::State)));

        this->advicement_label = new QLabel(this);

        int advicements_count = 7;
        this->current_advicement_index = 0;
        for (int i = 0; i < advicements_count; i++)
        {
            QTextBrowser* advicement = new QTextBrowser(this);
            advicement->setFixedSize(5336/scale, 592/scale);
            QFont font = advicement->font();
            font.setPointSize((int)180/scale);
            advicement->setFont(font);
            this->text_advicements.append(advicement);
            advicement->hide();
        }

        bool vertical = settings.value("vertical", true).toBool();
        this->showFullScreen();
        if (vertical)
        {
            this->setFixedSize(6244/scale, 10969/scale);

            this->bus_schedule->move(64/scale, 64/scale);
            this->bus_schedule->setFixedSize(2000/scale, 4356/scale);
            this->bus_schedule->verticalHeader()->setDefaultSectionSize(400/scale);
            this->bus_schedule->setColumnWidth(0, 900/scale);
            this->bus_schedule->setColumnWidth(1, 1100/scale);
            this->bus_schedule->setRowCount(11);

            this->picture_krasnoyarsk->setFixedSize(800/scale, 1000/scale);
            this->picture_krasnoyarsk->move(2300/scale, 64/scale);

            this->news_label_temperature->setFixedSize(1800/scale, 473/scale);
            this->news_label_temperature->move(4400/scale, 64/scale);
    //        news_label_temperature->setStyleSheet("QLabel { background-color:#FFFFFF}");

            this->news_label_time->setFixedSize(1800/scale, 473/scale);
            this->news_label_time->move(4400/scale, 570/scale);
    //        news_label_time->setStyleSheet("QLabel { background-color:#FFFFFF}");

            this->news_text->setFixedSize(3900/scale, 3480/scale);
            this->news_text->move(2200/scale, 1200/scale);
    //        news_text->setStyleSheet("QTextBrowser { background-color:#FFFFFF}");
        }
        else // horizontal
        {
            this->setFixedSize(10969/scale, 6244/scale);

            this->bus_schedule->move(64/scale, 64/scale);
    //        this->bus_schedule->setFixedSize((1090+1364)/scale, 6120/scale);
            this->bus_schedule->setColumnWidth(0, 1090/scale);
            this->bus_schedule->setColumnWidth(1, 1364/scale);
            this->bus_schedule->verticalHeader()->setDefaultSectionSize(400/scale);
            this->bus_schedule->setRowCount(10);

            this->picture_krasnoyarsk->setFixedSize(800/scale, 1000/scale);
            this->picture_krasnoyarsk->move(2640/scale, 116/scale);

            this->news_label_temperature->setFixedSize(1100/scale, 473/scale);
            this->news_label_temperature->move(3440/scale, 116/scale);
    //        news_label_temperature->setStyleSheet("QLabel { background-color:#FFFFFF}");

            this->news_label_time->setFixedSize(1330/scale, 450/scale);
            this->news_label_time->move(3440/scale, 592/scale);
    //        news_label_time->setStyleSheet("QLabel { background-color:#FFFFFF}");

            this->news_text->setFixedSize(2200/scale, 4700/scale);
            this->news_text->move(2650/scale, 1353/scale);
    //        news_text->setStyleSheet("QTextBrowser { background-color:#FFFFFF}");
        }

        this->news_label_temperature->setText("");

        this->loader = new ContentLoader();
        this->task_manager = new TaskManager(this, loader);
    }
    QTimer *timer = new QTimer(this);
    connect(timer, SIGNAL(timeout()), this, SLOT(off()));
    timer->start(60*1000);

}

int MainWindow::isNight() {
    QTime now_t = QTime::currentTime();
    now_t = QTime(now_t.hour(), now_t.minute()); // strip seconds
    QTime on_t = QTime::fromString(settings.value("start_work_time", "08:00:00").toString(),
                                   "hh:mm:ss");
    QTime off_t = QTime::fromString(settings.value("stop_work_time", "22:00:00").toString(),
                                    "hh:mm:ss");
    if (now_t == on_t || now_t == off_t)
        return MainWindow::OFF; // выключение

    else if (now_t >= off_t || now_t <= on_t)
        return MainWindow::NIGHT; // черный экран

    return MainWindow::DAY;
}

void MainWindow::off() {    
    if (this->isNight() == MainWindow::OFF)
        qApp->exit();
}

void MainWindow::displayImage(QString path)
{
    this->displayImage(this->video_view, path);
}

void MainWindow::stopAll()
{
    if (this->video_player)
        this->video_player->stop();
}

void MainWindow::displayImage(QGraphicsView *view, QString path)
{
    this->video_player->stop();
    view->scene()->clear();
    view->scene()->setSceneRect(view->rect());

    QPixmap image(path);
    view->scene()->addPixmap(image.scaled(view->size()));
    view->show();
}

void MainWindow::displayVideo(QString path)
{
    this->video_player->stop();
    this->video_view->scene()->clear();
    this->video_view->scene()->setSceneRect(this->video_view->rect());

    QGraphicsVideoItem* item = new QGraphicsVideoItem;
    item->setSize(this->video_view->size());
    this->video_player->setVideoOutput(item);
    this->video_view->scene()->addItem(item);
    this->video_view->show();

    this->video_player->setMedia(QUrl::fromLocalFile(path));
    this->video_player->play();
}

void MainWindow::displayNextAdvicement(QString text)
{
    this->text_advicements[this->current_advicement_index]->setText(text.replace("\n", " "));
    this->current_advicement_index = (this->current_advicement_index + 1) % this->current_advicement_size;
}


MainWindow::~MainWindow()
{
}

void MainWindow::player_state_changed(QMediaPlayer::State state)
{
    if (state == QMediaPlayer::StoppedState)
        emit this->video_finished();
}

void MainWindow::setBus(QMap<QString, int> buses)
{
    QList<QString> keys = buses.keys();
    if (keys.size() < 1)
        return;

    int count_item_in_bus_schedule = this->bus_schedule->rowCount();

    QSettings settings;
    float scale = settings.value("scale", 10.0).toFloat();
    QFont font = this->news_label_temperature->font();

    // хедеры вставил в нулевые строки, дабы не иметь проблем со стилями,
    // автобусы вставляются с первой ячейки
    font.setPointSize(160/(int)scale);
    font.setBold(false);
    TableItemDelegate* h_item = new TableItemDelegate(QString("Маршрут"), 0, font);
    this->bus_schedule->setItem(0, 0, h_item);

    h_item = new TableItemDelegate(QString("Ближайший"), 1, font);
    this->bus_schedule->setItem(0, 1, h_item);

    if (keys.length() < count_item_in_bus_schedule)
        count_item_in_bus_schedule = keys.length();
    this->bus_schedule->setRowCount(count_item_in_bus_schedule + 1); // +1 (хедеры)

    for (int i = 0; i < count_item_in_bus_schedule; i++)
    {
        if (buses[keys[i]] == 0)
            continue;
        font.setPointSize(350/(int)scale);
        font.setBold(true);
        TableItemDelegate* bus = new TableItemDelegate(QString("%1").arg(buses[keys[i]]), 0, font);
        this->bus_schedule->setItem(i+1, 0, bus);

        font.setPointSize(250/(int)scale);
        QTime t = QTime::fromString(keys[i], "hh:mm:ss"); // убрал секунды
        TableItemDelegate* next_time = new TableItemDelegate(QString(t.toString("hh:mm")), 1, font);
        this->bus_schedule->setItem(i+1, 1, next_time);
    }
    this->bus_schedule->sortByColumn(1, Qt::AscendingOrder);
}



void MainWindow::updateLabels(QString temperature)
{
    if (temperature != "") { // добавил значок градуса
        temperature = temperature.split(" ")[0] + QChar(176) + temperature.split(" ")[1];
    }
    this->news_label_temperature->setText(temperature);
    this->news_label_time->setText(QTime::currentTime().toString("hh:mm"));
}

void MainWindow::setNews(QString news_text){
    this->news_text->setText("<h1 align=\"center\">НОВОСТИ</h1>" + news_text);
    this->news_text->setVerticalScrollBarPolicy(Qt::ScrollBarAlwaysOff);
    this->news_text->setHorizontalScrollBarPolicy(Qt::ScrollBarAlwaysOff);
}


void MainWindow::setDisplayMode(MainWindow::DisplayMode mode){
    QSettings settings;
    int scale = settings.value("scale", 10).toInt();
    bool vertical = settings.value("vertical", true).toBool();

    if (vertical) {
        if(mode == MainWindow::ALL) {
            this->current_advicement_size = 3;
            this->video_view->show();
            this->video_view->setFixedSize(6544/scale, 4000/scale);
            this->video_view->move(0/scale, 4850/scale);

            /*
            this->advicement_label->setStyleSheet("QLabel { background-color:#D9D9D9}");
            this->advicement_label->setFixedSize(4244/scale, 2500/scale);
            this->advicement_label->move(0/scale, 8500/scale);*/

            int start_y_pos = 9060/scale;
            for (int i=0; i<this->current_advicement_size; i++) {
                this->text_advicements[i]->setFixedSize(5320/scale, 592/scale);
                this->text_advicements[i]->move(540/scale, start_y_pos + i*700/scale);
                this->text_advicements[i]->setVerticalScrollBarPolicy(Qt::ScrollBarAlwaysOff);
                this->text_advicements[i]->setHorizontalScrollBarPolicy(Qt::ScrollBarAlwaysOff);
                QFont font = this->text_advicements[i]->font();
                font.setPointSize(400/scale);
                this->text_advicements[i]->setFont(font);
                this->text_advicements[i]->show();
            }
            for (int i=this->current_advicement_size;i<this->text_advicements.size(); i++)
                this->text_advicements[i]->hide();

        }
        if(mode == MainWindow::TEXT){
            this->current_advicement_size = 7;
            this->video_view->hide();

            /*this->advicement_label->setStyleSheet("QLabel { background-color:#D9D9D9}");
            this->advicement_label->setFixedSize(6244/scale, 6150/scale);
            this->advicement_label->move(0/scale, 4850/scale);*/

            int start_y_pos = 5400/scale;
            for (int i=0; i<this->text_advicements.size(); i++) {
                this->text_advicements[i]->setVerticalScrollBarPolicy(Qt::ScrollBarAlwaysOff);
                this->text_advicements[i]->setHorizontalScrollBarPolicy(Qt::ScrollBarAlwaysOff);
                QFont font = this->text_advicements[i]->font();
                font.setPointSize(400/scale);
                this->text_advicements[i]->setFont(font);
                this->text_advicements[i]->setFixedSize(5320/scale, 592/scale);
                this->text_advicements[i]->move(540/scale, start_y_pos + i*700/scale);
                this->text_advicements[i]->show();
            }
        }
    }
    else {
        if(mode == MainWindow::ALL) {
            this->current_advicement_size = 3;
            this->video_view->show();
            this->video_view->setFixedSize(6428/scale, 3454/scale);
            this->video_view->move(4730/scale, 0/scale);

            this->advicement_label->setStyleSheet("QLabel { background-color:#D9D9D9}");
            this->advicement_label->setFixedSize(6428/scale, 2805/scale);
            this->advicement_label->move(4870/scale, 3455/scale);

            int start_y_pos = 3817;
            for (int i=0; i<this->current_advicement_size; i++) {
                this->text_advicements[i]->setFixedSize(5336/scale, 592/scale);
                this->text_advicements[i]->move(5192/scale, start_y_pos/scale + i*726/scale);
                this->text_advicements[i]->show();
            }
            for (int i=this->current_advicement_size;i<this->text_advicements.size(); i++)
                this->text_advicements[i]->hide();

        }
        if(mode == MainWindow::TEXT){
            this->current_advicement_size = 7;
            this->video_view->hide();

            this->advicement_label->setStyleSheet("QLabel { background-color:#D9D9D9}");
            this->advicement_label->setFixedSize(6428/scale, 6244/scale);
            this->advicement_label->move(4870/scale, 0/scale);

            int start_y_pos = 726/scale;
            for (int i=0; i<this->text_advicements.size(); i++) {
                this->text_advicements[i]->show();
                this->text_advicements[i]->setFixedSize(5336/scale, 592/scale);
                this->text_advicements[i]->move(5192/scale, start_y_pos + i*726/scale);
                this->text_advicements[i]->show();
            }
        }
    }

}
