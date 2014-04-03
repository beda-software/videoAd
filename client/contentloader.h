#ifndef CONTENTLOADER_H
#define CONTENTLOADER_H

#include <QObject>
#include <QHash>
#include <QSettings>
#include <QtXml/QDomDocument>
#include <QtNetwork/QNetworkRequest>
#include <QtNetwork/QNetworkAccessManager>
#include <QtNetwork/QNetworkReply>
#include <QEventLoop>
#include <QStringList>

#include <QDebug>
#include <QDateTime>

struct news{
    QString title;
    QDateTime date;
    QString full_text;
};

class ContentLoader : public QObject
{
    Q_OBJECT
public:
    ContentLoader(QObject *parent = 0);

    QString LoadNews();
    QMap<QString, int> LoadBus();
    QString LoadTemperature();


private:
    QNetworkAccessManager* manager;
    QByteArray request_get(QString url);


    int bus_stop_number;
};

#endif // CONTENTLOADER_H
