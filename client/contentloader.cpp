#include "contentloader.h"

ContentLoader::ContentLoader(QObject *parent) :
    QObject(parent)
{
    QSettings settings;
    this->manager = new QNetworkAccessManager(this);
    this->bus_stop_number = settings.value("bus_stop_number", 1).toInt();
}

QMap<int, QString> ContentLoader::LoadBus()
{
    QString url = QString("http://mu-kgt.ru/externalservice/strittv/getStopArriveTime.php?stop=%1").arg(this->bus_stop_number);
    QString data = this->request_get(url);

    data = "<html>" + data + "</html>";

    QDomDocument document;
    QString errors;
    if (!document.setContent(data, &errors))
        qDebug() << errors;

    QDomElement doc_elem = document.documentElement();
    QDomNodeList node_list = doc_elem.elementsByTagName("row");
    QMap<int, QString> result;
    for (int i = 0; i < node_list.length(); i++)
    {
        QString text = node_list.at(i).toElement().text();
        QStringList parts = text.split(",");
        result[parts[1].toInt()] = parts[3];
    }

    return result;
}

QByteArray ContentLoader::request_get(QString url)
{
    QNetworkRequest request(url);
    QNetworkReply* reply = this->manager->get(request);
    QEventLoop loop;
    connect(reply, SIGNAL(finished()), &loop, SLOT(quit()));
    loop.exec();

    QByteArray data = reply->readAll();
    return data;
}
