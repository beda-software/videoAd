#ifndef TABLEITEMDELEGATE_H
#define TABLEITEMDELEGATE_H

#include <QTableWidgetItem>

class TableItemDelegate : public QTableWidgetItem
{
public:
    TableItemDelegate(QString text, int column, QFont font);
};

#endif // TABLEITEMDELEGATE_H
