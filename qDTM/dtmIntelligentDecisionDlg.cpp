//ldldld

#include "dtmIntelligentDecisionDlg.h"
#include "ui_intelligentDecisionDlg.h"

dtmIntelligentDecisionDlg::dtmIntelligentDecisionDlg(QWidget* parent/*=nullptr*/)
	: QDialog(parent, Qt::Tool)
	, m_ui(new Ui::IntelligentDecisionDialog )
{
	m_ui->setupUi(this);

}

dtmIntelligentDecisionDlg::~dtmIntelligentDecisionDlg()
{
	delete m_ui;
}


