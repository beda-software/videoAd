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


class ContentLoader : public QObject
{
    Q_OBJECT
public:
    ContentLoader(QObject *parent = 0);

    QString LoadNews();
    QMap<int, QString> LoadBus();


private:
    QNetworkAccessManager* manager;
    QByteArray request_get(QString url);


    int bus_stop_number;
};

#endif // CONTENTLOADER_H
