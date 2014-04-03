#include "tableitemdelegate.h"

TableItemDelegate::TableItemDelegate(QString text, int column, QFont font)
{
    QTableWidgetItem::setData(Qt::DisplayRole, text);
    QTableWidgetItem::setTextAlignment(Qt::AlignCenter);
    QTableWidgetItem::setSizeHint(QSize(110, 40));

    if (column == 0) {
        font.setPixelSize(22);
        QTableWidgetItem::setBackgroundColor(QColor(255, 238, 221));
        QTableWidgetItem::setFont(font);
        QTableWidgetItem::setTextColor(QColor(20, 70, 125));
    }
    else if (column == 1) {
        QTableWidgetItem::setBackgroundColor(QColor(255, 255, 255));
        font.setBold(false);
        font.setPixelSize(22);
        QTableWidgetItem::setFont(font);
    }
}
