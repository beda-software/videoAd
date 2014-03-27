#include "mainwindow.h"
#include "ui_mainwindow.h"

MainWindow::MainWindow(QWidget *parent) :
    QMainWindow(parent),
    ui(new Ui::MainWindow)
{
    ui->setupUi(this);

    this->bus_schedule = new QTableWidget();


    this->news_label_temperature = new QLabel("-2C");
    this->news_label_temperature->setAlignment(Qt::AlignHCenter | Qt::AlignVCenter);
    this->news_label_time = new QLabel("14:88");
    this->news_label_time->setAlignment(Qt::AlignHCenter | Qt::AlignVCenter);
    this->news_text = new QTextEdit();
    this->news_box = new QVBoxLayout();

    QHBoxLayout* news_labels = new QHBoxLayout();
    news_labels->addWidget(this->news_label_temperature);
    news_labels->addWidget(this->news_label_time);

    this->news_box->addWidget(news_labels);
    this->news_box->addWidget(this->news_text);

    this->video_view = new QGraphicsView();

}

MainWindow::~MainWindow()
{
    delete ui;
}
