#include "contentloader.h"
#include <QXmlStreamReader>
#include <QDateTime>

ContentLoader::ContentLoader(QObject *parent) :
    QObject(parent)
{
    QSettings settings;
    this->manager = new QNetworkAccessManager(this);
    this->bus_stop_number = settings.value("bus_stop_number", 1).toInt();
}

QMap<QString, int> ContentLoader::LoadBus()
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
    QMap<QString, int> result;
    for (int i = 0; i < node_list.length(); i++)
    {
        QString text = node_list.at(i).toElement().text();
        QStringList parts = text.split(",");
        result[parts[3]] = parts[1].toInt();
    }

    return result;
}

QString ContentLoader::LoadNews(){
    QByteArray data = this->request_get("http://krasnoyarsk.sibnovosti.ru/rss");
    QXmlStreamReader xml;
    xml.addData(data);

    QList<news> news_list;
    news current;
    QString currentTag;
    QString result;

    int index=0;

    while (!xml.atEnd()) {
        index ++;
        xml.readNext();
        if (xml.isStartElement()){
            currentTag = xml.name().toString();
            //qDebug() << currentTag;
        } else if (xml.isEndElement()){
            currentTag = "";
            if(xml.name()=="item"){
                     //qDebug()<< current.title << current.date << current.full_text;
                     news_list << current;
                     current.title="";
                     current.date=QDateTime::currentDateTime();
                     current.full_text="";

            }
        } else if (xml.isCharacters()){

                if (currentTag == "title")
                    current.title = xml.text().toString();
                else if(currentTag == "full-text"){
                    if (current.full_text.length() < 300)
                    current.full_text += xml.text().toString();
                    //qDebug() << currentTag << xml.text();
                }
                else if(currentTag == "pubDate"){
                    current.date = QDateTime::fromString(xml.text().toString(),"ddd, d MMM yyyy hh:mm:ss");
                    qDebug() << current.date;
                }
            }
    }

    foreach(news item, news_list){
        result += "<h2>"+ item.title+"</h2><br/>"+item.full_text;
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

QString ContentLoader::LoadTemperature(){
    QByteArray data = this->request_get("http://export.yandex.ru/weather-ng/forecasts/29570.xml");
    QXmlStreamReader xml;
    QString currentTag;
    xml.addData(data);
    QString temperature = "";

    while (!xml.atEnd()) {
        xml.readNext();
        if (xml.isStartElement()){
            currentTag = xml.name().toString();
        } else if (xml.isEndElement()){
            currentTag = "";
            if(xml.name()=="fact"){
                return temperature + " C";
            }
        } else if (xml.isCharacters() && currentTag == "temperature")
            temperature = xml.text().toString();
    }
    return temperature;
}
