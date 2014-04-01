#-------------------------------------------------
#
# Project created by QtCreator 2014-03-27T12:10:14
#
#-------------------------------------------------


QT       += core widgets multimedia multimediawidgets xml network

TARGET = client
TEMPLATE = app


SOURCES += main.cpp\
        mainwindow.cpp \
    contentloader.cpp \
    taskmanager.cpp \
    tableitemdelegate.cpp

HEADERS  += mainwindow.h \
    contentloader.h \
    taskmanager.h \
    tableitemdelegate.h

FORMS    += mainwindow.ui

RESOURCES += \
    resources.qrc

