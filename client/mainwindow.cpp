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
    this->picture_krasnoyarsk->setMaximumSize(60, 80);
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

    this->text_box = new QVBoxLayout(this);
    int advicements_count = 3;
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

    this->DisplayImage(this->picture_krasnoyarsk, "kras.svg");
}


void MainWindow::DisplayImage(QGraphicsView *view, QString path)
{

}


MainWindow::~MainWindow()
{
    delete ui;
}
