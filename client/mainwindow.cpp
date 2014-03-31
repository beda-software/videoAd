#include "mainwindow.h"
#include "ui_mainwindow.h"


MainWindow::MainWindow(QWidget *parent) :
    QMainWindow(parent),
    ui(new Ui::MainWindow)
{
    QSettings settings;

    ui->setupUi(this);

    this->bus_schedule = new QTableWidget(1, 2, this);
    //this->bus_schedule->setSizePolicy(QSizePolicy::Minimum, QSizePolicy::Minimum);
    this->bus_schedule->setFrameStyle(QFrame::NoFrame);
    this->bus_schedule->viewport()->setAutoFillBackground(false);
    this->bus_schedule->setSizePolicy(QSizePolicy::Minimum, QSizePolicy::Minimum);
    this->bus_schedule->resizeColumnsToContents();
    this->bus_schedule->resizeRowsToContents();
    this->bus_schedule->verticalHeader()->hide();
    this->bus_schedule->horizontalHeader()->hide();

    this->news_label_temperature = new QLabel("--------", this);
    QFont label_font = this->news_label_temperature->font();
    label_font.setBold(true);
    label_font.setPointSize(30);
    this->news_label_temperature->setAlignment(Qt::AlignHCenter | Qt::AlignVCenter);
    this->news_label_time = new QLabel("--------", this);
    this->news_label_time->setAlignment(Qt::AlignHCenter | Qt::AlignVCenter);
    this->news_label_temperature->setFont(label_font);
    this->news_label_time->setFont(label_font);

    this->news_text = new QTextBrowser(this);
    this->news_text->setFrameStyle(QFrame::NoFrame);
    this->news_text->viewport()->setAutoFillBackground(false);

    QVBoxLayout* news_labels = new QVBoxLayout(this);
    news_labels->addWidget(this->news_label_temperature);
    news_labels->addWidget(this->news_label_time);


    this->picture_krasnoyarsk = new QGraphicsView(this);
    QGraphicsScene *picture_scene = new QGraphicsScene(this->picture_krasnoyarsk);
    this->picture_krasnoyarsk->setScene(picture_scene);

    QPixmap pixmap = QPixmap(":/images/krasnoyarsk.jpg");
    QGraphicsPixmapItem* item = new QGraphicsPixmapItem(pixmap.scaled(80,100));
    picture_scene->addItem(item);
    this->picture_krasnoyarsk->setMaximumSize(80, 100);
    this->picture_krasnoyarsk->setFrameStyle(QFrame::NoFrame);
    this->picture_krasnoyarsk->viewport()->setAutoFillBackground(false);

    QHBoxLayout* news_header = new QHBoxLayout(this);
    news_header->addWidget(this->picture_krasnoyarsk);
    news_header->addSpacerItem(new QSpacerItem(this->news_text->size().width()*3, 10, QSizePolicy::Maximum));
    news_header->addItem(news_labels);

    this->news_box = new QVBoxLayout(this);
    this->news_box->addLayout(news_header);
    this->news_box->addWidget(this->news_text);

    this->news_with_bus_schedule = new QHBoxLayout(this);
    this->news_with_bus_schedule->addWidget(this->bus_schedule);
    //this->news_with_bus_schedule->addSpacerItem(new QSpacerItem(100, 10, QSizePolicy::Maximum));
    this->news_with_bus_schedule->addLayout(this->news_box);


    this->video_view = new QGraphicsView(this);
    QGraphicsScene* scene = new QGraphicsScene;
    this->video_view->setScene(scene);
    this->video_view->setHorizontalScrollBarPolicy(Qt::ScrollBarAlwaysOff);
    this->video_view->setVerticalScrollBarPolicy(Qt::ScrollBarAlwaysOff);
    this->video_view->setFrameStyle(QFrame::NoFrame);
    this->video_view->viewport()->setAutoFillBackground(false);

    this->video_player = new QMediaPlayer(this);
    connect(this->video_player, SIGNAL(stateChanged(QMediaPlayer::State)), this, SLOT(player_state_changed(QMediaPlayer::State)));


    this->text_box = new QVBoxLayout(this);
    int advicements_count = 3;
    this->current_advicement_index = 0;
    for (int i = 0; i < advicements_count; i++)
    {
        QTextBrowser* advicement = new QTextBrowser(this);
        advicement->setSizePolicy(QSizePolicy::Minimum, QSizePolicy::Minimum);
        advicement->setMaximumHeight(50);
        this->text_advicements.append(advicement);
        this->text_box->addWidget(advicement);
    }


    bool vertical = settings.value("vertical",false).toBool();
    QLayout* main_layout;
    if (vertical)
    {
        main_layout = new QVBoxLayout(this);
        main_layout->addItem(this->news_with_bus_schedule);
        main_layout->addWidget(this->video_view);
        main_layout->addItem(this->text_box);
    }
    else // horizontal
    {   
        QVBoxLayout* video_with_advicements = new QVBoxLayout();
        video_with_advicements->addWidget(this->video_view);
        video_with_advicements->addItem(this->text_box);

        main_layout = new QHBoxLayout(this);
        main_layout->addItem(this->news_with_bus_schedule);
        main_layout->addItem(video_with_advicements);
    }

    ui->centralWidget->layout()->addItem(main_layout);

    this->news_label_temperature->setText("");
}

void MainWindow::displayImage(QString path)
{
    this->displayImage(this->video_view, path);
}

void MainWindow::stopAll()
{
    if (this->video_player)
        this->video_player->stop();

//    if (this->video_view->scene())
//        this->video_view->scene()->clear();
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
    this->text_advicements[this->current_advicement_index]->setText(text);
    this->current_advicement_index = (this->current_advicement_index + 1) % this->text_advicements.length();
}


MainWindow::~MainWindow()
{
    delete ui;
}

void MainWindow::player_state_changed(QMediaPlayer::State state)
{
    if (state == QMediaPlayer::StoppedState)
        emit this->video_finished();
}

void MainWindow::setBus(QMap<int, QString> buses)
{
    QFont item_font = this->news_label_temperature->font();
    item_font.setPixelSize(24);

    this->bus_schedule->clear();

    QList<int> keys = buses.keys();
    this->bus_schedule->setRowCount(keys.length());
    this->bus_schedule->setColumnCount(2);
    for (int i = 0; i < keys.length(); i++)
    {
        QTableWidgetItem* bus = new QTableWidgetItem(QString("%1").arg(keys[i]));
        bus->setFont(item_font);
        this->bus_schedule->setItem(i, 0, bus);

        QTableWidgetItem* next_time = new QTableWidgetItem(buses[keys[i]]);
        next_time->setFont(item_font);
        this->bus_schedule->setItem(i, 1, next_time);
    }

    this->bus_schedule->resizeRowsToContents();
    this->bus_schedule->resizeColumnsToContents();
}


void MainWindow::updateLabels(QString temperature)
{
    this->news_label_temperature->setText(temperature);
    this->news_label_time->setText(QTime::currentTime().toString("hh:mm"));
}

void MainWindow::setNews(QString news_text){
    this->news_text->setText(news_text);
    this->news_text->setVerticalScrollBarPolicy(Qt::ScrollBarAlwaysOff);
}
