// Example of a plugin action

#include "ccMainAppInterface.h"
#include <QtGui>
#include <QMessageBox>

namespace Test
{
	// This is an example of an action's method called when the corresponding action
	// is triggered (i.e. the corresponding icon or menu entry is clicked in CC's
	// main interface). You can access most of CC's components (database,
	// 3D views, console, etc.) via the 'appInterface' variable.
	void performActionA( ccMainAppInterface *appInterface )
	{
		if ( appInterface == nullptr )
		{
			// The application interface should have already been initialized when the plugin is loaded
			Q_ASSERT( false );
			
			return;
		}
		
		/*** HERE STARTS THE ACTION ***/
	
		// Put your code here
		// --> you may want to start by asking for parameters (with a custom dialog, etc.)
	
		QString dlgTitle = "Message Box";
		QString strInfo = "The file has opened!";
		QMessageBox::information(nullptr, dlgTitle, strInfo, QMessageBox::Ok, QMessageBox::NoButton);
		// This is how you can output messages
		// Display a standard message in the console
		appInterface->dispToConsole( "[TestPlugin] Hello world!", ccMainAppInterface::STD_CONSOLE_MESSAGE );
		
		// Display a warning message in the console
		appInterface->dispToConsole( "[TestPlugin] Warning: example plugin shouldn't be used as is", ccMainAppInterface::WRN_CONSOLE_MESSAGE );
		
		// Display an error message in the console AND pop-up an error box
		appInterface->dispToConsole( "Test plugin shouldn't be used - it doesn't do anything!", ccMainAppInterface::ERR_CONSOLE_MESSAGE );
	
		/*** HERE ENDS THE ACTION ***/
	}
}