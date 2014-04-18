#include "tableitemdelegate.h"
#include <QTime>

TableItemDelegate::TableItemDelegate(QString text, int column, QFont font)
{
    QTableWidgetItem::setData(Qt::DisplayRole, text);
    QTableWidgetItem::setTextAlignment(Qt::AlignCenter);
    QTableWidgetItem::setSizeHint(QSize(110, 40));

    if (column == 0) {
        QTableWidgetItem::setBackgroundColor(QColor(255, 238, 221));
        QTableWidgetItem::setFont(font);
        QTableWidgetItem::setTextColor(QColor(20, 70, 125));
    }
    else if (column == 1) {
        QTableWidgetItem::setBackgroundColor(QColor(255, 255, 255));
        QTableWidgetItem::setFont(font);
    }
}

bool TableItemDelegate::operator<(const QTableWidgetItem &other) const {
    QTime t1 = QTime::fromString(this->data(Qt::DisplayRole).toString(), "hh:mm");
    QTime t2 = QTime::fromString(other.data(Qt::DisplayRole).toString(), "hh:mm");

    if ((t1.hour() == 0 || t1.hour() == 1 || t1.hour() == 2) && (t2.hour() == 22 || t2.hour() == 23)) {
        return false;
    }
    if ((t2.hour() == 0 || t2.hour() == 1 || t2.hour() == 2) && (t1.hour() == 22 || t1.hour() == 23)) {
        return true;
    }
    return t1 < t2;
}
