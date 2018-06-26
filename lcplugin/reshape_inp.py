import os

def data_filter(s):
    data = list(filter(None,s.split(' ')))
    data = list(map(lambda s: s.strip(), data))
    data = list(filter(None,data))
    return data

def data_rebuild2Dict(Taget):
    sub_cor = {}
    for c in Taget:
        cor_l = []
        for ci in c[1:]:
            try:
                cor_l.append(float(ci))
            except:
                cor_l.append(ci)
        sub_cor[c[0]] = cor_l
    return sub_cor


def start_reshape(file_name):
    file = open(os.path.normpath(file_name),'r')
    title = []
    inp_dic = {}
    for s in file.readlines():
        if '[' in s and ']' in s:
            #title.append(s.strip()[1:-1])
            title = s.strip()[1:-1]
            inp_dic[title] = []
        else:
            data = data_filter(s)
            if len(data) != 0 and ';;' not in data[0]:
                inp_dic[title].append(data)


    inp_dic['COORDINATES'] = data_rebuild2Dict(inp_dic['COORDINATES'])  # coordinate rebuild to dict
    inp_dic['JUNCTIONS'] = data_rebuild2Dict(inp_dic['JUNCTIONS'])  # junction rebuild to dict
    inp_dic['OUTFALLS'] = data_rebuild2Dict(inp_dic['OUTFALLS'])  # outfall rebuild to dict
    try:
        inp_dic['STORAGE'] = data_rebuild2Dict(inp_dic['STORAGE'])  # storage rebuild to dict
    except:
        pass

    inp_dic['SUBAREAS'] = data_rebuild2Dict(inp_dic['SUBAREAS'])  # subcachment rebuild to dict
    inp_dic['INFILTRATION'] = data_rebuild2Dict(inp_dic['INFILTRATION'])  # infiltration rebuild to dict

    # conduit rebuild to dict
    sub_cond = {}
    for c in inp_dic['CONDUITS']:
        cor_l = []
        cor_l.append(c[1])  # inlet node must be string
        cor_l.append(c[2])  # outlet node must be string
        for ci in c[3:]:
            try:
                cor_l.append(float(ci))
            except:
                cor_l.append(ci)
        sub_cond[c[0]] = cor_l

    inp_dic['CONDUITS'] = sub_cond

    # SUBCATCHMENTS rebuild to dict
    sub_subc = {}
    for c in inp_dic['SUBCATCHMENTS']:
        cor_l = []
        cor_l.append(c[1])  # Rain Gage must be string
        cor_l.append(c[2])  # Outlet must be string
        for ci in c[3:]:
            cor_l.append(float(ci))
        sub_subc[c[0]] = cor_l

    inp_dic['SUBCATCHMENTS'] = sub_subc

    # TRANSECTS rebuild to dict
    transects_data = {}
    section = [[],[]]
    for d in inp_dic['TRANSECTS'][1:]:
        if d[0] == 'NC':    # Manning N
            nc = d[1:]
        elif d[0] == 'X1':  # link name
            link_name = d[1]
            transects_data[link_name] = {}
        elif d[0] == 'GR':  # section data
            for i,info in enumerate(d):
                if i != 0:
                    if i % 2 != 0:
                        section[1].append(round(float(info),4))
                    else:
                        section[0].append(round(float(info),4))
        
        if d[0] == ';' or d == inp_dic['TRANSECTS'][-1]:
            transects_data[link_name]['section'] = section
            transects_data[link_name]['NC'] = nc
            section = [[],[]]

    inp_dic['TRANSECTS'] = transects_data

    #polygon rebuild to dict
    sub_polygon = {}
    for d in inp_dic['Polygons']:
        coordinate = [float(d[1]),float(d[2])]
        if d[0] not in sub_polygon:  # if key not exist, create key in dict and append coordinate in to dict
            sub_polygon[d[0]] = []
            sub_polygon[d[0]].append(coordinate)
        else:  # if key exist, add coordinate in to dict
            sub_polygon[d[0]].append(coordinate)  

    inp_dic['Polygons'] = sub_polygon

    # the gravity center of polygon
    Polygon_center = {}
    for p in inp_dic['Polygons']:
        gcenter_x = 0
        gcenter_y = 0
        for pi in inp_dic['Polygons'][p]:
            gcenter_x += pi[0]/len(inp_dic['Polygons'][p])
            gcenter_y += pi[1]/len(inp_dic['Polygons'][p])
        Polygon_center[p] = [gcenter_x,gcenter_y]
    
    inp_dic['Polygon_center'] = Polygon_center

    sub_xsec = {}
    for xs in inp_dic['XSECTIONS']:
        sub_xsec[xs[0]] = {}
        sub_xsec[xs[0]]['Shape'] = xs[1]
        sub_xsec[xs[0]]['Information'] = xs[2:]

    inp_dic['XSECTIONS'] = sub_xsec

    # determination of road ditch
    epsilon = 0.03
    road_ditch = {}
    for sn in inp_dic['TRANSECTS']:
        road_ditch_info = []
        if len(inp_dic['TRANSECTS'][sn]['section'][0]) == len(inp_dic['TRANSECTS'][sn]['section'][1]):
            dl = len(inp_dic['TRANSECTS'][sn]['section'][0])
            x = inp_dic['TRANSECTS'][sn]['section'][0]
            y = inp_dic['TRANSECTS'][sn]['section'][1]
            for i in range(dl-3):
                cd1 = abs(x[i] - x[i+1]) <= epsilon
                cd2 = abs(y[i+1] - y[i+2]) <= epsilon
                cd3 = abs(x[i+2] - x[i+3]) <= epsilon
                cd4 = y[i+1] < y[i]
                cd5 = y[i+2] < y[i+3]
                if cd1 and cd2 and cd3 and cd4 and cd5:
                    road_ditch_info.append([round(x[i+2]-x[i+1],3),round(min(y[i]-y[i+1],y[i+3]-y[i+2]),3)])
            road_ditch[sn] = road_ditch_info
        else:
            print('error of data length')
    
    inp_dic['road_ditch'] = road_ditch
    
    return inp_dic
