project( CCQRibbon )

add_library( ${PROJECT_NAME} STATIC )

set_target_properties( ${PROJECT_NAME} PROPERTIES
    AUTOMOC OFF
    AUTORCC OFF
    AUTOUIC OFF
)


add_subdirectory( include )
add_subdirectory( src )

file( GLOB ui_list ui_templates/*.ui )
file( GLOB qrc_list *.qrc )

qt5_wrap_ui( generated_ui_list ${ui_list} )
qt5_add_resources( generated_qrc_list ${qrc_list} )