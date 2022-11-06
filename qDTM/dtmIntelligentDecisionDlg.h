//ldldld


#ifndef DTM_DECISION_DLG_HEADER
#define DTM_DECISION_DLG_HEADER

//Qt
#include <QDialog>


namespace Ui {
	class IntelligentDecisionDialog;
}

//! 智能决策对话框
class dtmIntelligentDecisionDlg : public QDialog
{
	Q_OBJECT

public:
	//! Default constructor
	dtmIntelligentDecisionDlg(QWidget* parent = nullptr);
	~dtmIntelligentDecisionDlg();

protected:



protected: //methods



protected: //members

private:
	Ui::IntelligentDecisionDialog* m_ui;
};

#endif
