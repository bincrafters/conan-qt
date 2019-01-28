[![Download](https://api.bintray.com/packages/bincrafters/public-conan/qt%3Abincrafters/images/download.svg) ](https://bintray.com/bincrafters/public-conan/qt%3Abincrafters/_latestVersion)
[![Build Status Travis](https://travis-ci.com/bincrafters/conan-qt.svg?branch=stable%2F5.12.0)](https://travis-ci.com/bincrafters/conan-qt)
[![Build Status AppVeyor](https://ci.appveyor.com/api/projects/status/github/bincrafters/conan-qt?branch=stable%2F5.12.0&svg=true)](https://ci.appveyor.com/project/bincrafters/conan-qt)

## Conan package recipe for [*qt*](https://www.qt.io)

Qt is a cross-platform framework for graphical user interfaces.

The packages generated with this **conanfile** can be found on [Bintray](https://bintray.com/bincrafters/public-conan/qt%3Abincrafters).


## Issues

If you wish to report an issue or make a request for a package, please do so here:

[Issues Tracker](https://github.com/bincrafters/community/issues)


## For Users

### Basic setup

    $ conan install qt/5.12.0@bincrafters/stable

### Project setup

If you handle multiple dependencies in your project is better to add a *conanfile.txt*

    [requires]
    qt/5.12.0@bincrafters/stable

    [generators]
    txt

Complete the installation of requirements for your project running:

    $ mkdir build && cd build && conan install ..

Note: It is recommended that you run conan install from a build directory and not the root of the project directory.  This is because conan generates *conanbuildinfo* files specific to a single build configuration which by default comes from an autodetected default profile located in ~/.conan/profiles/default .  If you pass different build configuration options to conan install, it will generate different *conanbuildinfo* files.  Thus, they should not be added to the root of the project, nor committed to git.


## Build and package

The following command both runs all the steps of the conan file, and publishes the package to the local system cache.  This includes downloading dependencies from "build_requires" and "requires" , and then running the build() method.

    $ conan create . bincrafters/stable


### Available Options
| Option        | Default | Possible Values  |
| ------------- |:----------------- |:------------:|
| shared      | True |  [True, False] |
| commercial      | False |  [True, False] |
| opengl      | desktop |  ['no', 'es2', 'desktop', 'dynamic'] |
| openssl      | True |  [True, False] |
| with_pcre2      | True |  [True, False] |
| with_doubleconversion      | True |  [True, False] |
| with_freetype      | True |  [True, False] |
| with_harfbuzz      | True |  [True, False] |
| with_libjpeg      | True |  [True, False] |
| with_libpng      | True |  [True, False] |
| with_sqlite3      | True |  [True, False] |
| with_pq      | True |  [True, False] |
| with_odbc      | True |  [True, False] |
| GUI      | True |  [True, False] |
| widgets      | True |  [True, False] |
| device      |  |  ANY |
| cross_compile      |  |  ANY |
| config      |  |  ANY |
| qtbase      | False |  [True, False] |
| qtbase_thread      | True |  [True, False] |
| qtbase_future      | True |  [True, False] |
| qtbase_concurrent      | True |  [True, False] |
| qtbase_iconv      | True |  [True, False] |
| qtbase_mimetype      | True |  [True, False] |
| qtbase_properties      | True |  [True, False] |
| qtbase_regularexpression      | True |  [True, False] |
| qtbase_sharedmemory      | True |  [True, False] |
| qtbase_systemsemaphore      | True |  [True, False] |
| qtbase_xmlstream      | True |  [True, False] |
| qtbase_xmlstreamreader      | True |  [True, False] |
| qtbase_xmlstreamwriter      | True |  [True, False] |
| qtbase_textdate      | True |  [True, False] |
| qtbase_datestring      | True |  [True, False] |
| qtbase_process      | True |  [True, False] |
| qtbase_processenvironment      | True |  [True, False] |
| qtbase_temporaryfile      | True |  [True, False] |
| qtbase_library      | True |  [True, False] |
| qtbase_settings      | True |  [True, False] |
| qtbase_filesystemwatcher      | True |  [True, False] |
| qtbase_filesystemiterator      | True |  [True, False] |
| qtbase_itemmodel      | True |  [True, False] |
| qtbase_proxymodel      | True |  [True, False] |
| qtbase_sortfilterproxymodel      | True |  [True, False] |
| qtbase_identityproxymodel      | True |  [True, False] |
| qtbase_stringlistmodel      | True |  [True, False] |
| qtbase_translation      | True |  [True, False] |
| qtbase_textcodec      | True |  [True, False] |
| qtbase_codecs      | True |  [True, False] |
| qtbase_big_codecs      | True |  [True, False] |
| qtbase_animation      | True |  [True, False] |
| qtbase_statemachine      | True |  [True, False] |
| qtbase_gestures      | True |  [True, False] |
| qtbase_sha3-fast      | True |  [True, False] |
| qtbase_timezone      | True |  [True, False] |
| qtbase_datetimeparser      | True |  [True, False] |
| qtbase_commandlineparser      | True |  [True, False] |
| qtbase_topleveldomain      | True |  [True, False] |
| qtbase_dtls      | True |  [True, False] |
| qtbase_ftp      | True |  [True, False] |
| qtbase_http      | True |  [True, False] |
| qtbase_udpsocket      | True |  [True, False] |
| qtbase_networkproxy      | True |  [True, False] |
| qtbase_socks5      | True |  [True, False] |
| qtbase_networkinterface      | True |  [True, False] |
| qtbase_networkdiskcache      | True |  [True, False] |
| qtbase_bearermanagement      | True |  [True, False] |
| qtbase_localserver      | True |  [True, False] |
| qtbase_dnslookup      | True |  [True, False] |
| qtbase_freetype      | True |  [True, False] |
| qtbase_sessionmanager      | True |  [True, False] |
| qtbase_texthtmlparser      | True |  [True, False] |
| qtbase_textodfwriter      | True |  [True, False] |
| qtbase_cssparser      | True |  [True, False] |
| qtbase_draganddrop      | True |  [True, False] |
| qtbase_shortcut      | True |  [True, False] |
| qtbase_action      | True |  [True, False] |
| qtbase_cursor      | True |  [True, False] |
| qtbase_clipboard      | True |  [True, False] |
| qtbase_wheelevent      | True |  [True, False] |
| qtbase_tabletevent      | True |  [True, False] |
| qtbase_im      | True |  [True, False] |
| qtbase_highdpiscaling      | True |  [True, False] |
| qtbase_validator      | True |  [True, False] |
| qtbase_standarditemmodel      | True |  [True, False] |
| qtbase_imageformatplugin      | True |  [True, False] |
| qtbase_movie      | True |  [True, False] |
| qtbase_imageformat_bmp      | True |  [True, False] |
| qtbase_imageformat_ppm      | True |  [True, False] |
| qtbase_imageformat_xbm      | True |  [True, False] |
| qtbase_imageformat_xpm      | True |  [True, False] |
| qtbase_imageformat_png      | True |  [True, False] |
| qtbase_imageformat_jpeg      | True |  [True, False] |
| qtbase_image_heuristic_mask      | True |  [True, False] |
| qtbase_image_text      | True |  [True, False] |
| qtbase_picture      | True |  [True, False] |
| qtbase_colornames      | True |  [True, False] |
| qtbase_pdf      | True |  [True, False] |
| qtbase_desktopservices      | True |  [True, False] |
| qtbase_systemtrayicon      | True |  [True, False] |
| qtbase_accessibility      | True |  [True, False] |
| qtbase_multiprocess      | True |  [True, False] |
| qtbase_whatsthis      | True |  [True, False] |
| qtbase_dom      | True |  [True, False] |
| qtbase_style-stylesheet      | True |  [True, False] |
| qtbase_effects      | True |  [True, False] |
| qtbase_filesystemmodel      | True |  [True, False] |
| qtbase_itemviews      | True |  [True, False] |
| qtbase_treewidget      | True |  [True, False] |
| qtbase_listwidget      | True |  [True, False] |
| qtbase_tablewidget      | True |  [True, False] |
| qtbase_abstractbutton      | True |  [True, False] |
| qtbase_commandlinkbutton      | True |  [True, False] |
| qtbase_datetimeedit      | True |  [True, False] |
| qtbase_stackedwidget      | True |  [True, False] |
| qtbase_textbrowser      | True |  [True, False] |
| qtbase_splashscreen      | True |  [True, False] |
| qtbase_splitter      | True |  [True, False] |
| qtbase_widgettextcontrol      | True |  [True, False] |
| qtbase_label      | True |  [True, False] |
| qtbase_formlayout      | True |  [True, False] |
| qtbase_lcdnumber      | True |  [True, False] |
| qtbase_menu      | True |  [True, False] |
| qtbase_lineedit      | True |  [True, False] |
| qtbase_radiobutton      | True |  [True, False] |
| qtbase_spinbox      | True |  [True, False] |
| qtbase_tabbar      | True |  [True, False] |
| qtbase_tabwidget      | True |  [True, False] |
| qtbase_combobox      | True |  [True, False] |
| qtbase_fontcombobox      | True |  [True, False] |
| qtbase_checkbox      | True |  [True, False] |
| qtbase_pushbutton      | True |  [True, False] |
| qtbase_toolbutton      | True |  [True, False] |
| qtbase_toolbar      | True |  [True, False] |
| qtbase_toolbox      | True |  [True, False] |
| qtbase_groupbox      | True |  [True, False] |
| qtbase_buttongroup      | True |  [True, False] |
| qtbase_mainwindow      | True |  [True, False] |
| qtbase_dockwidget      | True |  [True, False] |
| qtbase_mdiarea      | True |  [True, False] |
| qtbase_resizehandler      | True |  [True, False] |
| qtbase_statusbar      | True |  [True, False] |
| qtbase_menubar      | True |  [True, False] |
| qtbase_contextmenu      | True |  [True, False] |
| qtbase_progressbar      | True |  [True, False] |
| qtbase_abstractslider      | True |  [True, False] |
| qtbase_slider      | True |  [True, False] |
| qtbase_scrollbar      | True |  [True, False] |
| qtbase_dial      | True |  [True, False] |
| qtbase_scrollarea      | True |  [True, False] |
| qtbase_scroller      | True |  [True, False] |
| qtbase_graphicsview      | True |  [True, False] |
| qtbase_graphicseffect      | True |  [True, False] |
| qtbase_textedit      | True |  [True, False] |
| qtbase_syntaxhighlighter      | True |  [True, False] |
| qtbase_rubberband      | True |  [True, False] |
| qtbase_tooltip      | True |  [True, False] |
| qtbase_statustip      | True |  [True, False] |
| qtbase_sizegrip      | True |  [True, False] |
| qtbase_calendarwidget      | True |  [True, False] |
| qtbase_keysequenceedit      | True |  [True, False] |
| qtbase_dialog      | True |  [True, False] |
| qtbase_dialogbuttonbox      | True |  [True, False] |
| qtbase_messagebox      | True |  [True, False] |
| qtbase_colordialog      | True |  [True, False] |
| qtbase_filedialog      | True |  [True, False] |
| qtbase_fontdialog      | True |  [True, False] |
| qtbase_progressdialog      | True |  [True, False] |
| qtbase_inputdialog      | True |  [True, False] |
| qtbase_errormessage      | True |  [True, False] |
| qtbase_wizard      | True |  [True, False] |
| qtbase_dirmodel      | True |  [True, False] |
| qtbase_listview      | True |  [True, False] |
| qtbase_tableview      | True |  [True, False] |
| qtbase_treeview      | True |  [True, False] |
| qtbase_datawidgetmapper      | True |  [True, False] |
| qtbase_columnview      | True |  [True, False] |
| qtbase_paint_debug      | True |  [True, False] |
| qtbase_completer      | True |  [True, False] |
| qtbase_fscompleter      | True |  [True, False] |
| qtbase_undocommand      | True |  [True, False] |
| qtbase_undostack      | True |  [True, False] |
| qtbase_undogroup      | True |  [True, False] |
| qtbase_undoview      | True |  [True, False] |
| qtbase_cups      | True |  [True, False] |
| qtbase_printer      | True |  [True, False] |
| qtbase_printpreviewwidget      | True |  [True, False] |
| qtbase_printdialog      | True |  [True, False] |
| qtbase_printpreviewdialog      | True |  [True, False] |
| qtsvg      | False |  [True, False] |
| qtdeclarative      | False |  [True, False] |
| qtdeclarative_qml-network      | True |  [True, False] |
| qtdeclarative_qml-debug      | True |  [True, False] |
| qtdeclarative_qml-profiler      | True |  [True, False] |
| qtdeclarative_qml-preview      | True |  [True, False] |
| qtdeclarative_qml-devtools      | True |  [True, False] |
| qtdeclarative_qml-sequence-object      | True |  [True, False] |
| qtdeclarative_qml-list-model      | True |  [True, False] |
| qtdeclarative_qml-xml-http-request      | True |  [True, False] |
| qtdeclarative_qml-locale      | True |  [True, False] |
| qtdeclarative_qml-animation      | True |  [True, False] |
| qtdeclarative_qml-delegate-model      | True |  [True, False] |
| qtdeclarative_qml-worker-script      | True |  [True, False] |
| qtdeclarative_d3d12      | True |  [True, False] |
| qtdeclarative_quick-animatedimage      | True |  [True, False] |
| qtdeclarative_quick-canvas      | True |  [True, False] |
| qtdeclarative_quick-designer      | True |  [True, False] |
| qtdeclarative_quick-flipable      | True |  [True, False] |
| qtdeclarative_quick-gridview      | True |  [True, False] |
| qtdeclarative_quick-listview      | True |  [True, False] |
| qtdeclarative_quick-tableview      | True |  [True, False] |
| qtdeclarative_quick-particles      | True |  [True, False] |
| qtdeclarative_quick-path      | True |  [True, False] |
| qtdeclarative_quick-pathview      | True |  [True, False] |
| qtdeclarative_quick-positioners      | True |  [True, False] |
| qtdeclarative_quick-repeater      | True |  [True, False] |
| qtdeclarative_quick-shadereffect      | True |  [True, False] |
| qtdeclarative_quick-sprite      | True |  [True, False] |
| qtactiveqt      | False |  [True, False] |
| qtscript      | False |  [True, False] |
| qtmultimedia      | False |  [True, False] |
| qttools      | False |  [True, False] |
| qtxmlpatterns      | False |  [True, False] |
| qtxmlpatterns_xml-schema      | True |  [True, False] |
| qttranslations      | False |  [True, False] |
| qtdoc      | False |  [True, False] |
| qtrepotools      | False |  [True, False] |
| qtqa      | False |  [True, False] |
| qtlocation      | False |  [True, False] |
| qtlocation_location-labs-plugin      | True |  [True, False] |
| qtlocation_geoservices_osm      | True |  [True, False] |
| qtlocation_geoservices_here      | True |  [True, False] |
| qtlocation_geoservices_esri      | True |  [True, False] |
| qtlocation_geoservices_mapbox      | True |  [True, False] |
| qtlocation_geoservices_mapboxgl      | True |  [True, False] |
| qtlocation_geoservices_itemsoverlay      | True |  [True, False] |
| qtsensors      | False |  [True, False] |
| qtconnectivity      | False |  [True, False] |
| qtwayland      | False |  [True, False] |
| qt3d      | False |  [True, False] |
| qt3d_qt3d-render      | True |  [True, False] |
| qt3d_qt3d-input      | True |  [True, False] |
| qt3d_qt3d-logic      | True |  [True, False] |
| qt3d_qt3d-extras      | True |  [True, False] |
| qt3d_qt3d-animation      | True |  [True, False] |
| qt3d_qt3d-opengl-renderer      | True |  [True, False] |
| qtimageformats      | False |  [True, False] |
| qtgraphicaleffects      | False |  [True, False] |
| qtquickcontrols      | False |  [True, False] |
| qtserialbus      | False |  [True, False] |
| qtserialport      | False |  [True, False] |
| qtx11extras      | False |  [True, False] |
| qtmacextras      | False |  [True, False] |
| qtwinextras      | False |  [True, False] |
| qtandroidextras      | False |  [True, False] |
| qtwebsockets      | False |  [True, False] |
| qtwebchannel      | False |  [True, False] |
| qtwebengine      | False |  [True, False] |
| qtwebengine_webengine-embedded-build      | True |  [True, False] |
| qtwebengine_webengine-pepper-plugins      | True |  [True, False] |
| qtwebengine_webengine-printing-and-pdf      | True |  [True, False] |
| qtwebengine_webengine-webchannel      | True |  [True, False] |
| qtwebengine_webengine-proprietary-codecs      | True |  [True, False] |
| qtwebengine_webengine-kerberos      | True |  [True, False] |
| qtwebengine_webengine-spellchecker      | True |  [True, False] |
| qtwebengine_webengine-native-spellchecker      | True |  [True, False] |
| qtwebengine_webengine-webrtc      | True |  [True, False] |
| qtcanvas3d      | False |  [True, False] |
| qtwebview      | False |  [True, False] |
| qtquickcontrols2      | False |  [True, False] |
| qtquickcontrols2_quickcontrols2-fusion      | True |  [True, False] |
| qtquickcontrols2_quickcontrols2-imagine      | True |  [True, False] |
| qtquickcontrols2_quickcontrols2-material      | True |  [True, False] |
| qtquickcontrols2_quickcontrols2-universal      | True |  [True, False] |
| qtquickcontrols2_quicktemplates2-hover      | True |  [True, False] |
| qtquickcontrols2_quicktemplates2-multitouch      | True |  [True, False] |
| qtpurchasing      | False |  [True, False] |
| qtcharts      | False |  [True, False] |
| qtdatavis3d      | False |  [True, False] |
| qtvirtualkeyboard      | False |  [True, False] |
| qtgamepad      | False |  [True, False] |
| qtscxml      | False |  [True, False] |
| qtscxml_scxml-ecmascriptdatamodel      | True |  [True, False] |
| qtspeech      | False |  [True, False] |
| qtnetworkauth      | False |  [True, False] |
| qtremoteobjects      | False |  [True, False] |
| qtwebglplugin      | False |  [True, False] |


## Add Remote

    $ conan remote add bincrafters "https://api.bintray.com/conan/bincrafters/public-conan"


## Conan Recipe License

NOTE: The conan recipe license applies only to the files of this recipe, which can be used to build and package qt.
It does *not* in any way apply or is related to the actual software being packaged.

[MIT](https://github.com/bincrafters/conan-qt/blob/stable/5.12.0/LICENSE.md)
