#include <QtWebEngineCore>
#include <QCoreApplication>

int main(int argc, char *argv[]){
    QCoreApplication app(argc, argv);
    QCoreApplication::setApplicationName("Application Example");
    QCoreApplication::setApplicationVersion("1.0.0");

    QWebEngineHttpRequest httpRequest;

    return 0;
}
