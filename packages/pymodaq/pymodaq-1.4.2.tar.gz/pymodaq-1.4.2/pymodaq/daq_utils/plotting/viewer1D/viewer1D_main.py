from PyQt5 import QtGui, QtWidgets
from PyQt5.QtCore import Qt,QObject, pyqtSlot, QThread, pyqtSignal, QLocale, QDateTime, QSize
import sys
from pymodaq.daq_utils.plotting.viewer1D.viewer1D_GUI_dock import Ui_Form
from pymodaq.daq_measurement.daq_measurement_main import DAQ_Measurement
from collections import OrderedDict
from pymodaq.daq_utils.plotting.crosshair import Crosshair
import pyqtgraph as pg
import numpy as np
from pyqtgraph.parametertree import Parameter, ParameterTree
import pyqtgraph.parametertree.parameterTypes as pTypes
import pymodaq.daq_utils.custom_parameter_tree as customparameter
from pymodaq.daq_utils import daq_utils as utils
from pymodaq.daq_utils.plotting.viewer1D.viewer1Dbasic import Viewer1DBasic
import os
import pickle
import time

class Viewer1D(QtWidgets.QWidget,QObject):
    """this plots 1D data on a plotwidget. Math and measurement can be done on it. Datas and measurements are then exported with the signal
    data_to_export_signal
    """

    data_to_export_signal=pyqtSignal(OrderedDict) #self.data_to_export=edict(data0D=None,data1D=None,data2D=None)
    math_signal=pyqtSignal(OrderedDict) #OrderedDict:=[x_axis=...,data=...,ROI_bounds=...,operation=]
    ROI_changed=pyqtSignal()
    ROI_changed_finished=pyqtSignal()

    def __init__(self, parent=None):
        QLocale.setDefault(QLocale(QLocale.English, QLocale.UnitedStates))
        super(Viewer1D, self).__init__()

        if parent is None:
            parent=QtWidgets.QWidget()
        self.parent=parent
        self.ui=Ui_Form()
        self.ui.setupUi(parent)
        if DAQ_Measurement is None:
            self.ui.do_measurements_pb.setVisible(False)
        self.viewer_type='Data1D'
        self.legend = None
        #creating the settings widget of the viewer (ROI...)

        self.ui.settings_layout=QtWidgets.QVBoxLayout()
        horlayout=QtWidgets.QHBoxLayout()
        self.ui.load_ROI_pb=QtWidgets.QPushButton('Load')
        self.ui.save_ROI_pb=QtWidgets.QPushButton('Save')
        horlayout.addWidget(self.ui.save_ROI_pb)
        horlayout.addWidget(self.ui.load_ROI_pb)
        self.ui.settings_layout.addLayout(horlayout)
        self.ui.ROIs_widget.setLayout(self.ui.settings_layout)
        self.ui.ROIs_widget.setVisible(False)

        widg = QtWidgets.QWidget()
        self.viewer = Viewer1DBasic(widg)
        self.ui.verticalLayout.addWidget(widg)
        self.ui.Graph1D = self.viewer #for backcompatibility

        self.ui.statusbar=QtWidgets.QStatusBar(parent)
        self.ui.statusbar.setMaximumHeight(15)
        self.ui.StatusBarLayout.addWidget(self.ui.statusbar)


        #create and set the zoom widget
        #self.ui.zoom_widget=Dock("1DViewer zoom", size=(300, 100), closable=True)
        self.ui.zoom_widget=QtWidgets.QWidget()
        layout=QtWidgets.QHBoxLayout()


        self.ui.Graph_zoom=pg.PlotWidget()
        layout.addWidget(self.ui.Graph_zoom)
        self.ui.zoom_widget.setLayout(layout)

        self.ui.zoom_region=pg.LinearRegionItem()
        self.ui.zoom_region.setZValue(-10)
        self.ui.zoom_region.setBrush('r')
        self.ui.zoom_region.setOpacity(0.2)
        self.ui.Graph_zoom.addItem(self.ui.zoom_region)
        self.zoom_plot=[]
        #self.dockarea.addDock(self.ui.zoom_widget)
        self.ui.zoom_widget.setVisible(False)

        self.ui.xaxis_item=self.viewer.plotwidget.plotItem.getAxis('bottom')
        self.ui.Graph_Lineouts.hide()
        self.wait_time=3000
        self.measurement_module=None


        ##crosshair
        self.ui.crosshair = Crosshair(self.viewer.plotwidget.plotItem,orientation='vertical')
        self.ui.crosshair.crosshair_dragged.connect(self.update_crosshair_data)
        self.ui.crosshair_pb.clicked.connect(self.crosshairClicked)
        self.crosshairClicked()

        self._labels = []
        self.plot_channels = None
        self.plot_colors = utils.plot_colors
        self.color_list = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (14, 207, 189), (207, 14, 166), (207, 204, 14)]
        self.linear_regions = []
        self.lo_items = []
        self.lo_data = []
        self.ROI_bounds = []

        self._x_axis = None

        self.datas = []  # datas on each channel. list of 1D arrays
        self.data_to_export = OrderedDict(data0D=OrderedDict(), data1D=OrderedDict(), data2D=None)
        self.measurement_dict = OrderedDict(x_axis=None, data=None, ROI_bounds=None, operation=None)
        # OrderedDict to be send to the daq_measurement module
        self.measure_data_dict = OrderedDict()
        # dictionnary with data to be put in the table on the form: key="Meas.{}:".format(ind)
        # and value is the result of a given lineout or measurement

        # self.ui.Measurement_widget=Dock("Measurement Module", size=(300, 100), closable=True)
        # self.dockarea.addDock(self.ui.Measurement_widget)
        self.ui.Measurement_widget = QtWidgets.QWidget()
        self.ui.Measurement_widget.setVisible(False)

        # create viewer parameter tree

        self.ui.settings_tree = ParameterTree()

        self.ui.settings_layout.addWidget(self.ui.settings_tree)
        self.ui.settings_tree.setMinimumWidth(250)
        params = [
            {'title': 'Math Settings', 'name': 'math_settings', 'type': 'group', 'children': [
                {'title': 'Do math on CH:', 'name': 'channel_combo', 'type': 'list'},
                {'title': 'Math type:', 'name': 'math_function', 'type': 'list', 'values': ['Sum', 'Mean', 'half-life', 'expotime'],
                 'value': 'Sum'},
                {'title': 'N Lineouts:', 'name': 'Nlineouts_sb', 'type': 'int', 'value': 0, 'default': 0, 'min': 0},
                {'title': 'Spread ROI', 'name': 'spreadROI_pb', 'type': 'action'},
                {'title': 'Clear Lineouts', 'name': 'clear_lo_pb', 'type': 'action'}
            ]},
            {'name': 'Measurements', 'type': 'table', 'value': OrderedDict([]), 'Ncol': 2, 'header': ["LO", "Value"]},
            {'name': 'ROIs', 'type': 'group'}
        ]

        self.roi_settings = Parameter.create(title='Viewer Settings',name='Viewer1D_Settings', type='group', children=params)

        #connecting from tree
        self.roi_settings.child('math_settings', 'spreadROI_pb').sigActivated.connect(self.spread_lineouts)
        self.roi_settings.child('math_settings', 'clear_lo_pb').sigActivated.connect(self.clear_lo)


        self.ui.settings_tree.setParameters(self.roi_settings, showTop=False)
        self.roi_settings.sigTreeStateChanged.connect(self.roi_tree_changed)

        ##Connecting buttons:
        self.ui.Do_math_pb.clicked.connect(self.do_math_fun)
        self.ui.do_measurements_pb.clicked.connect(self.open_measurement_module)
        self.ui.zoom_pb.clicked.connect(self.enable_zoom)

        self.ui.save_ROI_pb.clicked.connect(self.save_ROI)
        self.ui.load_ROI_pb.clicked.connect(self.load_ROI)



    def add_lineout(self):
        ind=len(self.linear_regions)+1
        xbounds=self.viewer.plotwidget.plotItem.vb.viewRange()[0]
        roi_bounds=np.linspace(xbounds[0],xbounds[1],4*ind+1)
        item=pg.LinearRegionItem([roi_bounds[4*ind-1],roi_bounds[4*ind]])
        item.setZValue(-10)
        item.setBrush(QtGui.QColor(*self.color_list[ind-1]))
        item.setOpacity(0.2)
        self.linear_regions.append(item)
        self.viewer.plotwidget.plotItem.addItem(item)
        item.sigRegionChanged.connect(self.update_lineouts)
        item.sigRegionChangeFinished.connect(self.ROI_changed_finished.emit)

        item_lo=self.ui.Graph_Lineouts.plot()
        item_lo.setPen(QtGui.QColor(*self.color_list[ind-1]))
        self.lo_items.append(item_lo)
        child={'name': 'ROI_%02.0d' % ind, 'type': 'group', 'children': [
                {'name': 'Color', 'type': 'color', 'value': QtGui.QColor(*self.color_list[ind-1])},
                {'name': 'x1', 'type': 'float', 'value': item.getRegion()[0], 'step':1},
                {'name': 'x2', 'type': 'float', 'value': item.getRegion()[0], 'step':1}
                ]
               }
        self.roi_settings.sigTreeStateChanged.disconnect(self.roi_tree_changed)
        self.roi_settings.child('ROIs').addChild(child)
        self.roi_settings.sigTreeStateChanged.connect(self.roi_tree_changed)

    def change_lo_source(self,ind):
        try:
            if  type(ind) is pTypes.ListParameter:
                ind=ind.value()
            self.measurement_dict['data']=self.datas[ind]
            self.math_signal.emit(self.measurement_dict)  # OrderedDict:=[x_axis=...,data=...,ROI_bounds=...,operation=]
            if self.ui.do_measurements_pb.isChecked():
                self.update_measurement_module()
            self.math_signal.emit(self.measurement_dict)

        except:
            pass

        
    def clear_lo(self):
        self.lo_data=[[] for ind in range(len(self.lo_data))]
        self.update_lineouts()

    def crosshairClicked(self):
        if self.ui.crosshair_pb.isChecked():
            self.ui.crosshair.setVisible(True)
            self.ui.x_label.setVisible(True)
            self.ui.y_label.setVisible(True)
            range=self.viewer.plotwidget.plotItem.vb.viewRange()
            self.ui.crosshair.set_crosshair_position(xpos=np.mean(np.array(range[0])))
        else:
            self.ui.crosshair.setVisible(False)
            self.ui.x_label.setVisible(False)
            self.ui.y_label.setVisible(False)


    def do_math_fun(self):
        try:
            if self.ui.Do_math_pb.isChecked():
                self.ui.ROIs_widget.show()
                self.ui.Graph_Lineouts.show()
                self.update_N_lineouts(self.roi_settings.child('math_settings','Nlineouts_sb').value())
                try:
                    self.measurement_dict['x_axis']=self._x_axis
                    self.measurement_dict['data']=self.datas[self.roi_settings.child('math_settings','channel_combo').value()]
                    self.measurement_dict['ROI_bounds']=[item.getRegion() for item in self.linear_regions]
                    self.measurement_dict['operation']=self.roi_settings.child('math_settings','math_function').value()
                    #if hasattr(self,'math_thread'):
                    #    self.math_thread.quit()

                    self.math_object=Viewer1D_math()
                    #self.math_thread=QThread()
                    #math_object.moveToThread(self.math_thread)

                    self.math_signal[OrderedDict].connect(self.math_object.get_data)
                    self.math_object.math_sig[list].connect(self.show_math)


                    #self.math_thread.math_object=math_object
                    #self.math_thread.start()

                except Exception as e:
                    self.update_status(str(e),wait_time=self.wait_time)


            else:
                if hasattr(self,'math_thread'):
                    self.math_thread.quit()
                    del(self.math_thread)

                self.ui.Graph_Lineouts.hide()
                self.ui.ROIs_widget.hide()
                for item in self.linear_regions:
                    item.setVisible(False)

        except Exception as e:
            self.update_status(str(e),wait_time=self.wait_time)

    def do_zoom(self):
        bounds=self.ui.zoom_region.getRegion()
        self.viewer.plotwidget.setXRange(bounds[0],bounds[1])

    def enable_zoom(self):
        try:
            if not(self.ui.zoom_pb.isChecked()):
                if self.zoom_plot!=[]:
                    for plot in self.zoom_plot:
                        self.ui.Graph_zoom.removeItem(plot)
                self.ui.zoom_widget.hide()
                self.ui.zoom_region.sigRegionChanged.disconnect(self.do_zoom)

            else:
                self.zoom_plot=[]
                for ind,data in enumerate(self.datas):
                    channel=self.ui.Graph_zoom.plot()
                    channel.setPen(self.plot_colors[ind])
                    self.zoom_plot.append(channel)
                self.update_Graph1D(self.datas)
                self.ui.zoom_region.setRegion([np.min(self._x_axis),np.max(self._x_axis)])

                self.ui.zoom_widget.show()
                self.ui.zoom_region.sigRegionChanged.connect(self.do_zoom)
        except Exception as e:
            self.update_status(str(e),self.wait_time)

    def ini_data_plots(self, Nplots):
        self.plot_channels=[]
        self.legend = self.viewer.plotwidget.plotItem.addLegend()
        channels = []
        for ind in range(Nplots):
            channel=self.viewer.plotwidget.plot()
            channel.setPen(self.plot_colors[ind])
            self.legend.addItem(channel, self._labels[ind])
            channels.append(ind)
            self.plot_channels.append(channel)
        if Nplots > 0:
            self.roi_settings.child('math_settings','channel_combo').setOpts(limits=channels)
            self.roi_settings.child('math_settings','channel_combo').setValue(channels[0])

    def update_labels(self, labels):
        try:
            items = [item[1].text for item in self.legend.items]
            for item in items:
                self.legend.removeItem(item)

            if len(labels) == len(self.plot_channels):
                for ind, channel in enumerate(self.plot_channels):
                    self.legend.addItem(channel, self._labels[ind])
        except:
            self.update_status('plot channels not yet declared', wait_time=self.wait_time)

    @property
    def labels(self):
        return self._labels

    @labels.setter
    def labels(self, labels):
        self._labels = labels
        self.update_labels(labels)



    def load_ROI(self):
        try:
            self.roi_settings.child('math_settings', 'Nlineouts_sb').setValue(0)

            path=self.select_file(save=False)
            with open(path, 'rb') as f:
                data_tree = pickle.load(f)
                self.restore_state(data_tree)

        except Exception as e:
            pass

    def open_measurement_module(self):
        if not(self.ui.Do_math_pb.isChecked()):
            self.ui.Do_math_pb.setChecked(True)
            QtWidgets.QApplication.processEvents()
            self.ui.Do_math_pb.clicked.emit()
            QtWidgets.QApplication.processEvents()

        #self.ui.Measurement_widget.float()
        self.ui.Measurement_widget.setVisible(True)
        if self.ui.do_measurements_pb.isChecked():
            Form = self.ui.Measurement_widget
            self.measurement_module=DAQ_Measurement(Form)
            #self.ui.Measurement_widget.addWidget(Form)
            self.measurement_module.measurement_signal[list].connect(self.show_measurement)
            self.update_measurement_module()

        elif self.measurement_module is not None:
            self.measurement_module.Quit_fun()

    def remove_lineout(self):
        item=self.linear_regions.pop()
        self.viewer.plotwidget.plotItem.removeItem(item)
        item=self.lo_items.pop()
        self.ui.Graph_Lineouts.removeItem(item)
        self.roi_settings.child('ROIs').children()[-1].remove()
    #@pyqtSlot(str)

    def remove_plots(self):
        if self.plot_channels is not None:
            for channel in self.plot_channels:
                self.viewer.plotwidget.removeItem(channel)
            self.plot_channels = None
        if self.legend is not None:
            self.viewer.plotwidget.removeItem(self.legend)

    def restore_state(self,data_tree):
        self.roi_settings.restoreState(data_tree)
        QtWidgets.QApplication.processEvents()
        data_roi_dict=data_tree['children']['ROIs']['children']
        for k,v in data_roi_dict.items():
            for k2,v2 in data_roi_dict[k]['children'].items():
                self.roi_settings.child('ROIs',k,k2).setValue(v2['value'])

    def roi_tree_changed(self,param,changes):

        for param, change, data in changes:
            if change == 'value':

                if param.name() == 'Color' or param.name() == 'x1' or param.name() == 'x2' :
                    self.update_roi(param.parent(),param)
                elif param.name() == 'Nlineouts_sb':
                    self.update_N_lineouts(param.value())
                elif param.name() == 'channel_combo':
                    self.change_lo_source(param.value())
                elif param.name() == 'math_function':
                    self.update_measurement_type(param.value())
                # elif param.name() == 'ROIs':
                #     self.update_roi()



    def save_ROI(self):

        try:
            data=self.roi_settings.saveState()
            path=self.select_file()
            if path is not None:
                with open(path, 'wb') as f:
                    pickle.dump(data, f, pickle.HIGHEST_PROTOCOL)
        except Exception as e:
            pass

    def select_file(self,start_path=None,save=True):
        try:
            if save:
                fname = QtWidgets.QFileDialog.getSaveFileName(None, 'Enter a .roi1D file name',start_path,"roi1D file (*.roi1D)")
            else:
                fname=QtWidgets.QFileDialog.getOpenFileName(None, 'Select a .roi1D file name',start_path,"roi1D file (*.roi1D)")
            fname=fname[0]
            if not( not(fname)): #execute if the user didn't cancel the file selection
                (head,filename)=os.path.split(fname)
                (filename,ext)=os.path.splitext(fname)
                fname=os.path.join(head,filename+".roi1D")
            return fname

        except Exception as e:
            pass


    def set_axis_label(self,axis_settings=dict(orientation='bottom',label='x axis',units='pxls')):
        axis=self.viewer.plotwidget.plotItem.getAxis(axis_settings['orientation'])
        axis.setLabel(text=axis_settings['label'], units=axis_settings['units'])

    @pyqtSlot(list)
    def show_data(self, datas):
        try:
            if self.labels == [] or len(self.labels) != len(datas):
                self._labels = ["CH{}".format(ind) for ind in range(len(datas))]

            self.data_to_export=OrderedDict(data0D=OrderedDict(), data1D=OrderedDict(), data2D=None)
            for ind,data in enumerate(datas):
                self.data_to_export['data1D']['CH{:03d}'.format(ind)] = OrderedDict()

            self.datas=datas
            if self.plot_channels == None: #initialize data and plots
                self.ini_data_plots(len(datas))
            elif len(self.plot_channels) != len(datas):
                self.remove_plots()
                self.ini_data_plots(len(datas))

            self.update_Graph1D(datas)
            if self.ui.do_measurements_pb.isChecked():
                self.update_measurement_module()
        except Exception as e:
            self.update_status(str(e),wait_time=self.wait_time)


    @pyqtSlot(list)
    def show_data_temp(self, datas):
        """f
        to plot temporary data, for instance when all pixels are not yet populated...
        """
        if self.labels == [] or len(self.labels) != len(datas):
            self._labels = ["CH{}".format(ind) for ind in range(len(datas))]
        self.datas=datas
        if self.plot_channels==None: #initialize data and plots
            self.ini_data_plots(len(datas))
        elif len(self.plot_channels)!=len(datas):
            self.remove_plots()
            self.ini_data_plots(len(datas))

        for ind_plot, data in enumerate(datas):
            if self._x_axis is None:
                self._x_axis = np.linspace(0, len(data), len(data), endpoint=False)
                x_axis = self._x_axis
            elif len(self._x_axis) != len(data):
                x_axis = np.linspace(0, len(data), len(data), endpoint=False)
            else:
                x_axis = self._x_axis

            self.plot_channels[ind_plot].setData(x=x_axis, y=data)

    @pyqtSlot(list)
    def show_math(self,data_lo):
        #self.data_to_export=OrderedDict(x_axis=None,y_axis=None,z_axis=None,data0D=None,data1D=None,data2D=None)

        for ind,res in enumerate(data_lo):
            self.measure_data_dict["Lineout{}:".format(ind)]=res
            self.data_to_export['data0D']['Measure_{:03d}'.format(ind)]=res
        self.roi_settings.child('Measurements').setValue(self.measure_data_dict)

        if not(self.ui.do_measurements_pb.isChecked()): #otherwise you export data from measurement
            self.data_to_export['acq_time_s'] = time.perf_counter()
            self.data_to_export_signal.emit(self.data_to_export)

        [xelt.append(yelt) for xelt,yelt in zip(self.lo_data,data_lo)]
        for ind,data in enumerate(self.lo_data):
            self.lo_items[ind].setData(y=data)

    @pyqtSlot(list)
    def show_measurement(self,data_meas):
        ind_offset=len(self.data_to_export['data0D'])
        for ind,res in enumerate(data_meas):
            self.measure_data_dict["Meas.{}:".format(ind)]=res
            self.data_to_export['data0D']['Measure_{:03d}'.format(ind+ind_offset)]=res
        self.roi_settings.child('Measurements').setValue(self.measure_data_dict)
        self.data_to_export['acq_time_s'] = time.perf_counter()
        self.data_to_export_signal.emit(self.data_to_export)

    def spread_lineouts(self):
        xbounds=self.viewer.plotwidget.plotItem.vb.viewRange()[0]
        roi_bounds=np.linspace(xbounds[0],xbounds[1],4*len(self.linear_regions))
        for ind,item in enumerate(self.linear_regions):
            item.setRegion([roi_bounds[4*ind],roi_bounds[4*ind+1]])
    


    def update_crosshair_data(self,posx,posy,name=""):
        try:
            indx=utils.find_index(self._x_axis,posx)[0][0]

            string="y="
            for data in self.datas:
                string+="{:.6e} / ".format(data[indx])
            self.ui.y_label.setText(string)
            self.ui.x_label.setText("x={:.6e} ".format(posx))

        except Exception as e:
            pass

    def update_Graph1D(self,datas):
        #self.data_to_export=OrderedDict(data0D=OrderedDict(),data1D=OrderedDict(),data2D=None)
        try:

            for ind_plot,data in enumerate(datas):
                if self._x_axis is None:
                    self._x_axis=np.linspace(0,len(data),len(data),endpoint=False)
                elif len(self._x_axis)!=len(data):
                    self._x_axis=np.linspace(0,len(data),len(data),endpoint=False)

                self.plot_channels[ind_plot].setData(x=self._x_axis,y=data)

                if self.ui.zoom_pb.isChecked():
                    self.zoom_plot[ind_plot].setData(x=self._x_axis,y=data)
                self.data_to_export['data1D']['CH{:03d}'.format(ind_plot)]['data']=data # to be saved or exported
                self.data_to_export['data1D']['CH{:03d}'.format(ind_plot)]['x_axis']=self._x_axis
            self.measurement_dict['data']=datas[self.roi_settings.child('math_settings','channel_combo').value()] # to be used in the measurement module
            if not self.ui.Do_math_pb.isChecked(): #otherwise math is done and then data is exported
                self.data_to_export['acq_time_s'] = time.perf_counter()
                self.data_to_export_signal.emit(self.data_to_export)
            else:
                self.math_signal.emit(self.measurement_dict)

        except Exception as e:
            self.update_status(str(e),self.wait_time)


    def update_lineouts(self):
        self.ROI_bounds=[item.getRegion() for item in self.linear_regions]
        self.roi_settings.sigTreeStateChanged.disconnect(self.roi_tree_changed)
        for ind,child in enumerate(self.roi_settings.child('ROIs').children()):
            child.child(('x1')).setValue(self.ROI_bounds[ind][0])
            child.child(('x2')).setValue(self.ROI_bounds[ind][1])
        self.roi_settings.sigTreeStateChanged.connect(self.roi_tree_changed)
        self.measurement_dict['ROI_bounds']=self.ROI_bounds
        self.math_signal.emit(self.measurement_dict) #OrderedDict:=[x_axis=...,data=...,ROI_bounds=...,operation=]
        self.ROI_changed.emit()


    def update_measurement_module(self):
        xdata=self.measurement_dict['x_axis']
        ydata=self.measurement_dict['data']
        if xdata is None:
            self.measurement_module.update_data(ydata=ydata)
        else:
            self.measurement_module.update_data(xdata=xdata,ydata=ydata)

    def update_measurement_type(self,operation):
        self.measurement_dict['operation']=operation
        self.math_signal.emit(self.measurement_dict) #OrderedDict:=[x_axis=...,data=...,ROI_bounds=...,operation=]

    def update_N_lineouts(self,Nlineouts):
        if type(Nlineouts) is customparameter.SimpleParameterCustom: #case when the parameter signal was launched
            Nlineouts=Nlineouts.value()
        self.measure_data_dict=OrderedDict([])

        flag=len(self.linear_regions)!=Nlineouts
        while flag:
            Nl=len(self.linear_regions)
            if Nl>Nlineouts:
                self.remove_lineout()
            elif Nl<Nlineouts:
                self.add_lineout()
            else:
                flag=False

        self.lo_data=[[] for ind in range(Nlineouts)]
        self.update_lineouts()

    def update_roi(self,parent,param):

        index_roi=self.roi_settings.child('ROIs').children().index(parent)
        if param.name() == 'Color':
            self.linear_regions[index_roi].setBrush(QtGui.QColor(param.value().rgba()))
            self.lo_items[index_roi].setPen(QtGui.QColor(param.value().rgba()))

        elif param.name() == 'x1':
            pos=self.linear_regions[index_roi].getRegion()
            self.linear_regions[index_roi].setRegion([param.value(),pos[1]])
        elif param.name() == 'x2':
            pos=self.linear_regions[index_roi].getRegion()
            self.linear_regions[index_roi].setRegion([pos[0],param.value()])

    def update_status(self,txt,wait_time=0):
        self.ui.statusbar.showMessage(txt,wait_time)

    @property
    def x_axis(self):
        return self._x_axis

    @x_axis.setter
    def x_axis(self, x_axis):
        label = 'Pxls'
        units = ''
        if isinstance(x_axis, dict):
            if 'data' in x_axis:
                xdata = x_axis['data']
            if 'label' in x_axis:
                label = x_axis['label']
            if 'units' in x_axis:
                units = x_axis['units']
        else:
            xdata=x_axis
        self._x_axis = xdata
        self.show_data_temp(self.datas)
        self.set_axis_label(dict(orientation='bottom', label=label, units=units))

class Viewer1D_math(QObject):
    status_sig = pyqtSignal(list)
    math_sig=pyqtSignal(list)

    #def __init__(self,measurement_dict):
    #    super(QObject,self).__init__()   
    #    self.data=measurement_dict['data']
    #    self.ROI_bounds=measurement_dict['ROI_bounds']
    #    self._x_axis=measurement_dict['x_axis']
    #    self.operation=measurement_dict['operation']
    def __init__(self):
        super(QObject,self).__init__()   
        self.data=None
        self.ROI_bounds=None
        self._x_axis=None
        self.operation=None
    
    @pyqtSlot(OrderedDict) #OrderedDict:=[x_axis=...,data=...,ROI_bounds=...,operation=]
    def get_data(self,measurement_dict):
        self.data=measurement_dict['data']
        self.ROI_bounds=measurement_dict['ROI_bounds']
        self._x_axis=measurement_dict['x_axis']
        self.operation=measurement_dict['operation']
        self.update_math()

    def update_math(self):
        #self.status_sig.emit(["Update_Status","doing math"])
        data_lo=[]
        for bounds in self.ROI_bounds:
            indexes=utils.find_index(self._x_axis,bounds)
            ind1=indexes[0][0]
            ind2=indexes[1][0]
            sub_data = self.data[ind1:ind2]
            sub_xaxis = self._x_axis[ind1:ind2]

            if self.operation=="Mean":
                data_lo.append(np.mean(sub_data))
            elif self.operation=="Sum":
                data_lo.append(np.sum(sub_data))
            elif self.operation == 'half-life' or self.operation == 'expotime':
                ind_x0 = utils.find_index(sub_data, np.max(sub_data))[0][0]
                x0 = sub_xaxis[ind_x0]
                sub_xaxis = sub_xaxis[ind_x0:]
                sub_data = sub_data[ind_x0:]
                offset = sub_data[-1]
                N0 = np.max(sub_data) - offset
                if self.operation == 'half-life':
                    time = sub_xaxis[utils.find_index(sub_data - offset, 0.5 * N0)[0][0]]-x0
                elif self.operation == 'expotime':
                    time = sub_xaxis[utils.find_index(sub_data - offset, 0.37 * N0)[0][0]] - x0
                data_lo.append(time)

        self.math_sig.emit(data_lo)



if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    Form=QtWidgets.QWidget()
    prog = Viewer1D(Form)

    from pymodaq.daq_utils.daq_utils import gauss1D
    x=np.linspace(0,200,201)
    y1=gauss1D(x,75,25)
    y2=gauss1D(x,120,50,2)
    tau_half = 27
    tau2=100
    x0=50
    dx=20
    ydata_expodec = np.zeros((len(x)))
    ydata_expodec[:50] = 1*gauss1D(x[:50],x0,dx,2)
    ydata_expodec[50:] = 1*np.exp(-(x[50:]-x0)/(tau_half/np.log(2)))#+1*np.exp(-(x[50:]-x0)/tau2)
    ydata_expodec += 0.1*np.random.rand(len(x))

    prog.show_data([y1, y2, ydata_expodec])
    Form.show()
    prog.x_axis
    sys.exit(app.exec_())

