// Example of a plugin action

#include "ccMainAppInterface.h"
#include <QtGui>
#include <QMessageBox>
#include <iostream>
#include <Python.h>
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
namespace generatePath
{	
	void performActionA( ccMainAppInterface *m_app )
	{
		assert(m_app);
if (!m_app)
	return;

//Py_SetPythonHome(L"E:/lib/Anaconda3/envs/xyz");
//Py_Initialize();
//PyRun_SimpleString("import sys");
//PyRun_SimpleString("sys.path.append('E:/project/DTM/CloudCompare-DTM/plugins/example/generatePathPlugin/py')");
//PyObject* pName = PyUnicode_FromString("TEST");
//PyObject* pModule = PyImport_Import(pName);
//
//PyObject* func1 = PyObject_GetAttrString(pModule, "GenPath");
// 
//PyObject* tuple1 = PyTuple_New(2);
//PyTuple_SetItem(tuple1, 0, PyUnicode_FromString("E:\\2D polygon2.stl"));
//PyTuple_SetItem(tuple1, 1, PyLong_FromLong(5));
//
//PyObject* poly = PyObject_CallObject(func1, tuple1);
// 
//PyObject* func2 = PyObject_GetAttrString(pModule, "writeAptFile");
//// 参数进栈  
//PyObject* tuple2 = PyTuple_New(3);
//PyTuple_SetItem(tuple2, 0, poly);
//PyTuple_SetItem(tuple2, 1, PyUnicode_FromString("E:\\2D polygon2.stl"));
//PyTuple_SetItem(tuple2, 2, PyUnicode_FromString("E:\\1.Apt"));
//
//PyObject_CallObject(func2, tuple2);
//
//Py_XDECREF(func1);
//Py_XDECREF(func2);
//Py_XDECREF(tuple1);
//Py_XDECREF(tuple2);
//Py_XDECREF(poly);
//Py_XDECREF(pName);
//Py_XDECREF(pModule);

//Py_Finalize();

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
for (int i = 0; i < num; i++)
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