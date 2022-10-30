# DigitalTwinManufacture example for standard plugins

# REPLACE ALL 'ExamplePlugin' OCCURENCES BY YOUR PLUGIN NAME
# AND ADAPT THE CODE BELOW TO YOUR OWN NEEDS!

# Add an option to CMake to control whether we build this plugin or not
option( PLUGIN_TEST_STANDARD "Install test plugin" OFF )

if ( PLUGIN_TEST_STANDARD )
	project( TestPlugin )
	 
	AddPlugin( NAME ${PROJECT_NAME} )
		
	add_subdirectory( include )
	add_subdirectory( src )
	
	# set dependencies to necessary libraries
	# target_link_libraries( ${PROJECT_NAME} LIB1 )

    find_package(PCL REQUIRED)

    link_directories( ${PCL_LIBRARY_DIRS} )
    add_definitions( ${PCL_DEFINITIONS} )
    target_link_libraries( ${PROJECT_NAME} ${PCL_LIBRARIES})
    set_property( TARGET ${PROJECT_NAME} APPEND PROPERTY COMPILE_DEFINITIONS LP_PCL_PATCH_ENABLED )
    include( ExportPCLDlls.cmake )
    export_PCL_dlls( ${CLOUDCOMPARE_DEST_FOLDER} )

endif()
