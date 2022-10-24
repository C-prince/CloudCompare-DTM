// Example of a plugin action

#include "ccMainAppInterface.h"
#include <QtGui>
#include <QMessageBox>
#include <iostream>
#include <pcl/io/pcd_io.h>
#include <pcl/io/ply_io.h>
#include <pcl/point_types.h>
#include <pcl/common/io.h>
#include <pcl/keypoints/iss_3d.h>
#include <pcl/features/normal_3d.h>
#include <pcl/visualization/pcl_visualizer.h>
#include <boost/thread/thread.hpp>
#include <pcl/visualization/cloud_viewer.h>

//qCC_db
#include <ccPointCloud.h>
#include <ccMesh.h>
#include <ccProgressDialog.h>
#include <ccScalarField.h>

using namespace std;
typedef pcl::PointXYZRGBA PointT;
typedef pcl::Normal PointNT;
namespace Test
{
	// This is an example of an action's method called when the corresponding action
	// is triggered (i.e. the corresponding icon or menu entry is clicked in CC's
	// main interface). You can access most of CC's components (database,
	// 3D views, console, etc.) via the 'appInterface' variable.
	void performActionA( ccMainAppInterface *m_app )
	{
	//	assert(m_app);
	//	if (m_app == nullptr)
	//	{
	//		// The application interface should have already been initialized when the plugin is loaded
	//		Q_ASSERT(false);

	//		return;
	//	}

	//
	//const ccHObject::Container& selectedEntities = m_app->getSelectedEntities();
	//ccPointCloud* cccloud = static_cast<ccPointCloud*>(m_app->getSelectedEntities()[0]);
 //	pcl::PointCloud<PointT>::Ptr cloud(new pcl::PointCloud<PointT>);
	//for (int i = 0; i < cccloud->size(); i++)
	//{
	//	//点云赋值
	//	PointT point;
	//	point.x = (cccloud->getPoint(i))->x;
	//	point.y = (cccloud->getPoint(i))->y;
	//	point.z = (cccloud->getPoint(i))->z;
	//	cloud->push_back(point);
	//}
	//	
	//	pcl::PointCloud<pcl::Boundary> boundaries;		//用于存储边界估计的结果
	//	pcl::BoundaryEstimation<PointT, PointNT, pcl::Boundary> be;		//创建一个估计器
	//	pcl::NormalEstimation<PointT, PointNT> ne;	//法向量估计对象
	//	pcl::PointCloud<PointNT>::Ptr normals(new pcl::PointCloud<PointNT>);		//存储法向量
	//	//pcl::PointCloud<PointT>::Ptr cloud_boundary(new pcl::PointCloud<PointT>);	//边界点

	//	//计算法向量
	//	ne.setInputCloud(cloud);
	//	ne.setRadiusSearch(0.05);
	//	ne.compute(*normals);

	//	//边界提取
	//	pcl::search::KdTree<PointT>::Ptr method(new pcl::search::KdTree<PointT>);
	//	be.setInputCloud(cloud);
	//	be.setInputNormals(normals);
	//	be.setRadiusSearch(0.05);
	//	be.setAngleThreshold(M_PI / 4);
	//	be.setSearchMethod(method);
	//	be.compute(boundaries);

	//	std::vector<ccHObject*> allCloud;
	//	ccPointCloud* ccBoundary = new ccPointCloud("BoundaryPoints");
	//	for (int i = 0; i < cloud->size(); i++)
	//	{
	//		if (boundaries[i].boundary_point > 0)
	//		{		//判断是否为边界点
	//			PointT tmp = cloud->points[i];
	//			ccBoundary->addPoint(CCVector3(tmp.x,
	//				tmp.y,
	//				tmp.z));
	//		}
	//	}

	//	ccBoundary->setColor(ccColor::Rgba(rand() % 255, rand() % 255, rand() % 255, 200));
	//	ccBoundary->showColors(true);
	//	ccBoundary->setPointSize(5);
	//	allCloud.push_back(ccBoundary);

	//	ccHObject* cloudGroup = new ccHObject(QString("CloudGroup"));
	//	for (int i = 0; i < allCloud.size(); i++) 
	//	{
	//		cloudGroup->addChild(allCloud[i]);
	//	}

	//	m_app->addToDB(cloudGroup);
	//	m_app->refreshAll();
	//	m_app->updateUI();

		assert(m_app);
if (!m_app)
	return;

const ccHObject::Container& selectedEntities = m_app->getSelectedEntities();
ccPointCloud* cccloud = static_cast<ccPointCloud*>(m_app->getSelectedEntities()[0]);
	pcl::PointCloud<PointT>::Ptr cloud(new pcl::PointCloud<PointT>);
   for (int i = 0; i < cccloud->size(); i++)
   {
   	//点云赋值
   	PointT point;
   	point.x = (cccloud->getPoint(i))->x;
   	point.y = (cccloud->getPoint(i))->y;
   	point.z = (cccloud->getPoint(i))->z;
   	cloud->push_back(point);
   }

   	pcl::ISSKeypoint3D<PointT, PointT> iss;
   	pcl::PointCloud<PointT>::Ptr keypoints(new pcl::PointCloud<PointT>());
   	pcl::search::KdTree<PointT>::Ptr tree(new pcl::search::KdTree<PointT>());

   	iss.setInputCloud(cloud);
   	iss.setSearchMethod(tree);
   	iss.setSalientRadius(2.5);//设置用于计算协方差矩阵的球邻域半径
   	iss.setNonMaxRadius(2.5);//设置非极大值抑制应用算法的半径
   	iss.setThreshold21(0.65); //设定第二个和第一个特征值之比的上限
   	iss.setThreshold32(0.5);  //设定第三个和第二个特征值之比的上限
   	iss.setMinNeighbors(10); //在应用非极大值抑制算法时，设置必须找到的最小邻居数
   	iss.setNumberOfThreads(4); //初始化调度器并设置要使用的线程数
   	iss.compute(*keypoints);

   	cout << "ISS_3D points number " << keypoints->points.size();
   	//pcl::io::savePCDFile("keypoints_iss_3d.pcd", *keypoints, true);

   	ccPointCloud* newcloud = new ccPointCloud("new");
   	int num = keypoints->points.size();
   	newcloud->reserve(static_cast<unsigned>(keypoints->size()));
   	newcloud->reserveTheRGBTable();
   	for (int i = 0; i <num ; i++)
   	{
   		CCVector3 Pxyz(keypoints->points[i].x, keypoints->points[i].y, keypoints->points[i].z);
   		ccColor::Rgb PRgb(keypoints->points[i].r, keypoints->points[i].g, keypoints->points[i].b);
   		newcloud->addPoint(Pxyz);
   		newcloud->addColor(PRgb);
   	}
   	m_app->addToDB(newcloud);
   	m_app->updateUI();
   	m_app->refreshAll();

	}
}