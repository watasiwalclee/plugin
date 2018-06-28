from qgis.core import *
from PyQt5.QtCore import QVariant
import os

def put_on_map(inp_Dict):
    EPSGid = '3826'
    '''
    TWD97:'3826'
    WGS84:'4326'
    '''
    Junction_layer = QgsVectorLayer('Point?crs=epsg:'+EPSGid,'Junction','memory')
    Storage_layer = QgsVectorLayer('Point?crs=epsg:'+EPSGid,'Storage','memory')
    Outfall_layer = QgsVectorLayer('Point?crs=epsg:'+EPSGid,'Outfall','memory')
    Road_layer = QgsVectorLayer('LineString?crs=epsg:'+EPSGid,'Road','memory')
    Sewer_layer = QgsVectorLayer('LineString?crs=epsg:'+EPSGid,'Sewer','memory')
    Channel_layer = QgsVectorLayer('LineString?crs=epsg:'+EPSGid,'Channel','memory')
    PolygonLink_layer = QgsVectorLayer('LineString?crs=epsg:'+EPSGid,'PolygonLink_layer','memory')
    RoadDitch_layer = QgsVectorLayer('LineString?crs=epsg:'+EPSGid,'RoadDitch_layer','memory')
    Polygon_layer = QgsVectorLayer('Polygon?crs=epsg:'+EPSGid,'Polygon','memory')

    node_cor = inp_Dict['COORDINATES']  # load inp information
    # add field for each layer
    Junction_layer.dataProvider().addAttributes([QgsField('Name',QVariant.String),
    QgsField('X',QVariant.Double),
    QgsField('Y',QVariant.Double),
    QgsField('Elevation',QVariant.Double),
    QgsField('Max Depth',QVariant.Double),
    QgsField('InitDepth',QVariant.Double),
    QgsField('SurDepth',QVariant.Double),
    QgsField('Aponded',QVariant.Double),])
    Junction_layer.updateFields()

    Outfall_layer.dataProvider().addAttributes([QgsField('Name',QVariant.String),
    QgsField('Elevation',QVariant.Double),
    QgsField('Type',QVariant.String),
    QgsField('Stage Data',QVariant.String),
    QgsField('Gated',QVariant.String),
    QgsField('Route To',QVariant.String),])
    Outfall_layer.updateFields()

    Storage_layer.dataProvider().addAttributes([QgsField('Name',QVariant.String),
    QgsField('Elevation',QVariant.Double),
    QgsField('Max Depth',QVariant.Double),
    QgsField('InitDepth',QVariant.Double),
    QgsField('Shape',QVariant.String),
    QgsField('Curve Name/Params',QVariant.String),
    QgsField('Fevap',QVariant.Double),
    QgsField('Psi',QVariant.Double),])
    Storage_layer.updateFields()

    Road_layer.dataProvider().addAttributes([QgsField('Name',QVariant.String),
    QgsField('From Node',QVariant.String),
    QgsField('To Node',QVariant.String),
    QgsField('Length',QVariant.Double),
    QgsField('Roughness',QVariant.Double),
    QgsField('InOffset',QVariant.Double),
    QgsField('OutOffset',QVariant.Double),
    QgsField('InitFlow',QVariant.Double),
    QgsField('MaxFlow',QVariant.Double),])
    Road_layer.updateFields()

    Sewer_layer.dataProvider().addAttributes([QgsField('Name',QVariant.String),
    QgsField('From Node',QVariant.String),
    QgsField('To Node',QVariant.String),
    QgsField('Length',QVariant.Double),
    QgsField('Roughness',QVariant.Double),
    QgsField('InOffset',QVariant.Double),
    QgsField('OutOffset',QVariant.Double),
    QgsField('InitFlow',QVariant.Double),
    QgsField('MaxFlow',QVariant.Double),])
    Sewer_layer.updateFields()

    Channel_layer.dataProvider().addAttributes([QgsField('Name',QVariant.String),
    QgsField('From Node',QVariant.String),
    QgsField('To Node',QVariant.String),
    QgsField('Length',QVariant.Double),
    QgsField('Roughness',QVariant.Double),
    QgsField('InOffset',QVariant.Double),
    QgsField('OutOffset',QVariant.Double),
    QgsField('InitFlow',QVariant.Double),
    QgsField('MaxFlow',QVariant.Double),])
    Channel_layer.updateFields()

    PolygonLink_layer.dataProvider().addAttributes([QgsField('From node',QVariant.String),
    QgsField('To node',QVariant.String)])
    PolygonLink_layer.updateFields()

    Polygon_layer.dataProvider().addAttributes([QgsField('Name',QVariant.String),
    QgsField('X',QVariant.Double),
    QgsField('Y',QVariant.Double),
    QgsField('Rain Gage',QVariant.String),
    QgsField('Outlet',QVariant.String),
    QgsField('Area',QVariant.String),
    QgsField('%Imperv',QVariant.String),
    QgsField('Width',QVariant.String),
    QgsField('%Slope',QVariant.String),
    QgsField('N-Imperv',QVariant.String),
    QgsField('N-Perv',QVariant.String),
    QgsField('S-Imperv',QVariant.String),
    QgsField('S-Perv',QVariant.String),
    QgsField('PctZero',QVariant.String),
    QgsField('RouteTo',QVariant.String),
    QgsField('CurveNum',QVariant.String),
    QgsField('Conductivity',QVariant.String),
    QgsField('DryTime',QVariant.String),])
    Polygon_layer.updateFields()

    # road ditch layer
    RoadDitch_layer.dataProvider().addAttributes([QgsField('Name',QVariant.String),
    QgsField('road_width',QVariant.Double),
    QgsField('ditch 1',QVariant.String),
    QgsField('ditch 2',QVariant.String),
    QgsField('ditch 3',QVariant.String),
    QgsField('ditch 4',QVariant.String),
    QgsField('ditch 5',QVariant.String),
    QgsField('ditch 6',QVariant.String),
    QgsField('ditch 7',QVariant.String),
    QgsField('ditch 8',QVariant.String),])
    RoadDitch_layer.updateFields()

    Junction_column = ['Name','X','Y','Elevation','Max Depth','InitDepth','SurDepth','Aponded']
    Storage_column = ['Name','Elevation','Max Depth','InitDepth','Shape','Curve Name/Params','Fevap','Psi']
    Link_column = ['Name','From Node','To Node','Length','Roughness','InOffset','OutOffset','InitFlow','MaxFlow']
    RoadDitch_column = ['ditch 1','ditch 2','ditch 3','ditch 4','ditch 5','ditch 6','ditch 7','ditch 8']

    # add point features
    for d in node_cor:
        if d in inp_Dict['JUNCTIONS']:
            Junction_feat = QgsFeature(Junction_layer.fields())  # create Feature Objects
            for i,jc in enumerate(Junction_column):  # set feature attribute
                if i == 1:
                    Junction_feat.setAttribute(jc,node_cor[d][0])
                elif i == 2:
                    Junction_feat.setAttribute(jc,node_cor[d][1])
                elif i != 0:
                    Junction_feat.setAttribute(jc,inp_Dict['JUNCTIONS'][d][i-3])
                else:
                    Junction_feat.setAttribute(jc,d)
            Junction_feat.setGeometry(QgsGeometry.fromPointXY(QgsPointXY(node_cor[d][0], 
            node_cor[d][1]))) # set point Geometry information in Feature Objects
            Junction_layer.dataProvider().addFeatures([Junction_feat])  # add feature to layer
        elif d in inp_Dict['OUTFALLS']:  # still have revised
            Outfall_feat = QgsFeature(Outfall_layer.fields())  # create Feature Objects
            Outfall_feat.setAttribute('Name',d) # set feature attribute
            Outfall_feat.setAttribute('Elevation',inp_Dict['OUTFALLS'][d][0])
            Outfall_feat.setAttribute('Type',inp_Dict['OUTFALLS'][d][1])
            Outfall_feat.setGeometry(QgsGeometry.fromPointXY(QgsPointXY(node_cor[d][0], 
            node_cor[d][1]))) # set point Geometry information in Feature Objects
            Outfall_layer.dataProvider().addFeatures([Outfall_feat])  # add feature to layer
        elif d in inp_Dict['STORAGE']:
            Storage_feat = QgsFeature(Storage_layer.fields())  # create Feature Objects
            for i,jc in enumerate(Storage_column):  # set feature attribute
                if i != 0:
                    Storage_feat.setAttribute(jc,inp_Dict['STORAGE'][d][i-3])
                else:
                    Storage_feat.setAttribute(jc,d)
            Storage_feat.setGeometry(QgsGeometry.fromPointXY(QgsPointXY(node_cor[d][0], 
            node_cor[d][1]))) # set point Geometry information in Feature Objects
            Storage_layer.dataProvider().addFeatures([Storage_feat])  # add feature to layer

    # add line features
    Conduit_dic = inp_Dict['CONDUITS']
    curb_epislon = 0.01
    for c in Conduit_dic:
        fromnode_cor = QgsPoint(node_cor[Conduit_dic[c][0]][0],node_cor[Conduit_dic[c][0]][1])
        tonode_cor = QgsPoint(node_cor[Conduit_dic[c][1]][0],node_cor[Conduit_dic[c][1]][1])
        Line_feat = QgsFeature(Road_layer.fields())  # 3 fields all of same
        for i,jc in enumerate(Link_column):  # set feature attribute
            if i != 0:
                Line_feat.setAttribute(jc,inp_Dict['CONDUITS'][c][i-1])
            else:
                Line_feat.setAttribute(jc,c)
        
        if c not in inp_Dict['VERTICES']:
            Line_feat.setGeometry(QgsGeometry.fromPolyline([fromnode_cor,tonode_cor]))
        else:
            vertice_node = []
            for vn in inp_Dict['VERTICES'][c]:
                vertice_node.append(QgsPoint(vn[0],vn[1]))
            Line_feat.setGeometry(QgsGeometry.fromPolyline([fromnode_cor]+vertice_node+[tonode_cor]))
        
        if inp_Dict['XSECTIONS'][c]['Shape'] == 'IRREGULAR':
            curb_left_check = abs(inp_Dict['TRANSECTS'][inp_Dict['XSECTIONS'][c]['Information'][0]]['section'][0][0] - 
            inp_Dict['TRANSECTS'][inp_Dict['XSECTIONS'][c]['Information'][0]]['section'][0][1])
            curb_right_check = abs(inp_Dict['TRANSECTS'][inp_Dict['XSECTIONS'][c]['Information'][0]]['section'][0][-1] - 
            inp_Dict['TRANSECTS'][inp_Dict['XSECTIONS'][c]['Information'][0]]['section'][0][-2])
            curb_left_check_2 = inp_Dict['TRANSECTS'][inp_Dict['XSECTIONS'][c]['Information'][0]]['section'][1][0] > inp_Dict['TRANSECTS'][inp_Dict['XSECTIONS'][c]['Information'][0]]['section'][1][2]
            curb_right_check_2 = inp_Dict['TRANSECTS'][inp_Dict['XSECTIONS'][c]['Information'][0]]['section'][1][-1] > inp_Dict['TRANSECTS'][inp_Dict['XSECTIONS'][c]['Information'][0]]['section'][1][-3]
            curb_left_check_3 = round(abs(inp_Dict['TRANSECTS'][inp_Dict['XSECTIONS'][c]['Information'][0]]['section'][1][0] - 
            inp_Dict['TRANSECTS'][inp_Dict['XSECTIONS'][c]['Information'][0]]['section'][1][1])) >= 3
            curb_right_check_3 = round(abs(inp_Dict['TRANSECTS'][inp_Dict['XSECTIONS'][c]['Information'][0]]['section'][1][-1] - 
            inp_Dict['TRANSECTS'][inp_Dict['XSECTIONS'][c]['Information'][0]]['section'][1][-2])) >= 3
            if ((curb_left_check < curb_epislon) and curb_left_check_2 and curb_left_check_3) or ((curb_right_check < curb_epislon) and curb_right_check_2 and curb_right_check_3):  # road
                Road_layer.dataProvider().addFeatures([Line_feat])
            else: # Channel
                Channel_layer.dataProvider().addFeatures([Line_feat])
        else: # Sewer
            Sewer_layer.dataProvider().addFeatures([Line_feat])

    # add polygon link feature
    try:
        # add Polygon features
        Polygon_dic = inp_Dict['Polygons']
        Subarea_dic = inp_Dict['SUBAREAS']
        infiltration_dic = inp_Dict['INFILTRATION']
        for c in Polygon_dic:
            Polygon_feat = QgsFeature(Polygon_layer.fields())
            Polygon_feat.setAttribute('Name',c)
            Polygon_feat.setAttribute('X',round(inp_Dict['Polygon_center'][c][0],3))
            Polygon_feat.setAttribute('Y',round(inp_Dict['Polygon_center'][c][1],3))
            Polygon_feat.setAttribute('Rain Gage',Subcatchment_dic[c][0])
            Polygon_feat.setAttribute('Outlet',Subcatchment_dic[c][1])
            Polygon_feat.setAttribute('Area',Subcatchment_dic[c][2])
            Polygon_feat.setAttribute('%Imperv',Subcatchment_dic[c][3])
            Polygon_feat.setAttribute('Width',Subcatchment_dic[c][4])
            Polygon_feat.setAttribute('%Slope',Subcatchment_dic[c][5])
            Polygon_feat.setAttribute('N-Imperv',Subarea_dic[c][0])
            Polygon_feat.setAttribute('N-Perv',Subarea_dic[c][1])
            Polygon_feat.setAttribute('S-Imperv',Subarea_dic[c][2])
            Polygon_feat.setAttribute('S-Perv',Subarea_dic[c][3])
            Polygon_feat.setAttribute('PctZero',Subarea_dic[c][4])
            Polygon_feat.setAttribute('RouteTo',Subarea_dic[c][5])
            Polygon_feat.setAttribute('CurveNum',infiltration_dic[c][0])
            Polygon_feat.setAttribute('Conductivity',infiltration_dic[c][1])
            Polygon_feat.setAttribute('DryTime',infiltration_dic[c][2])
            Polygon_point = [QgsPointXY(p[0],p[1]) for p in Polygon_dic[c]]
            Polygon_feat.setGeometry(QgsGeometry.fromPolygonXY([Polygon_point]))
            Polygon_layer.dataProvider().addFeatures([Polygon_feat])
        
        Subcatchment_dic = inp_Dict['SUBCATCHMENTS']
        if len(Subcatchment_dic) != 0:
            for s in Subcatchment_dic:
                SL_feat = QgsFeature(PolygonLink_layer.fields())
                SL_feat.setAttribute('From node',s)
                SL_feat.setAttribute('To node',Subcatchment_dic[s][1])
                fromnode_cor = QgsPoint(inp_Dict['Polygon_center'][s][0],inp_Dict['Polygon_center'][s][1])
                outlet_point = Subcatchment_dic[s][1]
                tonode_cor = QgsPoint(node_cor[outlet_point][0],node_cor[outlet_point][1])
                SL_feat.setGeometry(QgsGeometry.fromPolyline([fromnode_cor,tonode_cor]))
                PolygonLink_layer.dataProvider().addFeatures([SL_feat])
        path = os.path.dirname(os.path.abspath(__file__))
        PolygonLink_layer.loadNamedStyle(os.path.normpath(path)+'\\OutLet_Check.qml')
    except:
        pass
    
    
    # add road ditch features
    Road_ditch_dict = inp_Dict['road_ditch']
    for c in inp_Dict['XSECTIONS']:
        if inp_Dict['XSECTIONS'][c]['Shape'] == 'IRREGULAR':
            Line_feat = QgsFeature(RoadDitch_layer.fields())
            fromnode_cor = QgsPoint(node_cor[Conduit_dic[c][0]][0],node_cor[Conduit_dic[c][0]][1])
            tonode_cor = QgsPoint(node_cor[Conduit_dic[c][1]][0],node_cor[Conduit_dic[c][1]][1])
            Line_feat.setAttribute('Name',c)
            Line_feat.setAttribute('road_width',round(inp_Dict['TRANSECTS'][inp_Dict['XSECTIONS'][c]['Information'][0]]['section'][0][-1] - 
            inp_Dict['TRANSECTS'][inp_Dict['XSECTIONS'][c]['Information'][0]]['section'][0][0],3))
            for i,jc in enumerate(Road_ditch_dict[inp_Dict['XSECTIONS'][c]['Information'][0]]):  # set feature attribute
                Line_feat.setAttribute(RoadDitch_column[i],'Width:' + str(jc[0]) + '\nDepth:' + str(jc[1]))

            if c not in inp_Dict['VERTICES']:
                Line_feat.setGeometry(QgsGeometry.fromPolyline([fromnode_cor,tonode_cor]))
            else:
                vertice_node = []
                for vn in inp_Dict['VERTICES'][c]:
                    vertice_node.append(QgsPoint(vn[0],vn[1]))
                Line_feat.setGeometry(QgsGeometry.fromPolyline([fromnode_cor]+vertice_node+[tonode_cor]))
            
            RoadDitch_layer.dataProvider().addFeatures([Line_feat])


    
    try:
        QgsProject.instance().addMapLayer(Polygon_layer)
        QgsProject.instance().addMapLayer(PolygonLink_layer)
    except:
        pass
    QgsProject.instance().addMapLayer(RoadDitch_layer)
    QgsProject.instance().addMapLayer(Sewer_layer)
    QgsProject.instance().addMapLayer(Channel_layer)
    QgsProject.instance().addMapLayer(Road_layer)
    QgsProject.instance().addMapLayer(Outfall_layer)
    QgsProject.instance().addMapLayer(Storage_layer)
    QgsProject.instance().addMapLayer(Junction_layer)
    

