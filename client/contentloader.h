#ifndef CONTENTLOADER_H
#define CONTENTLOADER_H

#include <QHash>

class ContentLoader
{
public:
    ContentLoader();

    QString LoadNews();
    QHash<QString, QString> LoadBus();

};

#endif // CONTENTLOADER_H
