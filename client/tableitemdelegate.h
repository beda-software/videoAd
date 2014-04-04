#ifndef TABLEITEMDELEGATE_H
#define TABLEITEMDELEGATE_H

#include <QTableWidgetItem>

class TableItemDelegate : public QTableWidgetItem
{
public:
    TableItemDelegate(QString text, int column, QFont font);
    bool operator<(const QTableWidgetItem &other) const;
};

#endif // TABLEITEMDELEGATE_H
