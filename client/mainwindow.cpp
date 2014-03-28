#include "mainwindow.h"
#include "ui_mainwindow.h"


MainWindow::MainWindow(QWidget *parent) :
    QMainWindow(parent),
    ui(new Ui::MainWindow)
{
    ui->setupUi(this);

    this->bus_schedule = new QTableWidget(1, 2, this);
    this->bus_schedule->setSizePolicy(QSizePolicy::Minimum, QSizePolicy::Minimum);
    this->bus_schedule->resizeColumnsToContents();
    this->bus_schedule->resizeRowsToContents();
    this->bus_schedule->setFrameStyle(QFrame::NoFrame);
    this->bus_schedule->viewport()->setAutoFillBackground(false);

    this->news_label_temperature = new QLabel("-2C", this);
    this->news_label_temperature->setAlignment(Qt::AlignHCenter | Qt::AlignVCenter);
    this->news_label_time = new QLabel("14:88", this);
    this->news_label_time->setAlignment(Qt::AlignHCenter | Qt::AlignVCenter);
    this->news_text = new QTextBrowser(this);
    this->news_text->setFrameStyle(QFrame::NoFrame);
    this->news_text->viewport()->setAutoFillBackground(false);

    QVBoxLayout* news_labels = new QVBoxLayout(this);
    news_labels->addWidget(this->news_label_temperature);
    news_labels->addWidget(this->news_label_time);

    this->picture_krasnoyarsk = new QGraphicsView(this);
    this->picture_krasnoyarsk->setMaximumSize(80, 100);
    QHBoxLayout* news_header = new QHBoxLayout(this);
    news_header->addWidget(this->picture_krasnoyarsk);
    news_header->addSpacerItem(new QSpacerItem(1000, 10, QSizePolicy::Maximum));
    news_header->addItem(news_labels);

    this->news_box = new QVBoxLayout(this);
    this->news_box->addLayout(news_header);
    this->news_box->addWidget(this->news_text);

    this->news_with_bus_schedule = new QHBoxLayout(this);
    this->news_with_bus_schedule->addWidget(this->bus_schedule);
    this->news_with_bus_schedule->addSpacerItem(new QSpacerItem(100, 10, QSizePolicy::Maximum));
    this->news_with_bus_schedule->addLayout(this->news_box);

    this->video_view = new QGraphicsView(this);
    this->video_player = new QMediaPlayer(this);

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


    bool vertical = true;
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

        main_layout = new QHBoxLayout(this);
        main_layout->addItem(this->news_with_bus_schedule);
        main_layout->addWidget(this->video_view);
    }

    ui->verticalLayout->addItem(main_layout);

    this->displayImage(this->video_view, "kras.svg");

    this->displayNextAdvicement(tr("Сегодня в красноярске был пойман педофил"));
    this->displayNextAdvicement(tr("Ололо ололо а я быдло и хуйло!\n89313451345"));
    this->displayNextAdvicement(tr("Ололо ололо а я быдло и хуйло!\n89313451345"));
    this->displayNextAdvicement(tr("Ололо ололо а я быдло и хуйло!\n89313451345"));

    this->displayVideo("AlexD.mp4");
}


void MainWindow::displayImage(QGraphicsView *view, QString path)
{
    QGraphicsScene* scene;
    if (view->scene())
    {
        view->scene()->clear();
        scene = view->scene();
    }
    else
    {
        scene = new QGraphicsScene(view);
    }

    scene->setSceneRect(view->rect());
    view->setScene(scene);
    QPixmap image(path);
    scene->addPixmap(image.scaled(view->size()));
    view->show();
}

void MainWindow::displayVideo(QString path)
{
    if (!this->video_view->scene())
        this->video_view->setScene(new QGraphicsScene(this->video_view));
    else
        this->video_view->scene()->clear();

    QGraphicsVideoItem* item = new QGraphicsVideoItem;
    this->video_player->setVideoOutput(item);
    if (!this->video_view->scene())
        this->video_view->setScene(new QGraphicsScene(this->video_view));
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
