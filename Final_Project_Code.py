import arcpy
import numpy as np
import pandas as pd
import os

##allow overwriting
arcpy.env.overwriteOutput = True

##Create GDB
arcpy.management.CreateFileGDB(r"C:\Users\Eli_G\Desktop\project","project.gdb")

##set workspace
arcpy.env.workspace = r"C:\Users\Eli_G\Desktop\project\project.gdb"


#add other block files

arcpy.conversion.FeatureClassToFeatureClass("" +"MOE_RGNS_polygon.shp","","regions")
arcpy.conversion.FeatureClassToFeatureClass(""+"VRI_clip.shp","","vridata")
arcpy.conversion.FeatureClassToFeatureClass(""+ "FWLKSPL_polygon.shp","","lakes")


#variables

VRI = "" + "vridata"
region = "" +"regions"
lakes = ""+"lakes"

print(VRI)
print(region)
print(lakes)


#list field names for VRI
fieldList = arcpy.ListFields(VRI)
for field in fieldList:
    print(field.name)
    
#delete fields
dropFields = ["FEATURE_CL","INVENTORY_","SURFACE_EX","MODIFYING_","SITE_POSIT","SOIL_NUTRI",
              "ECOSYS_CLA","INTERPRETE", "SPECIAL_CR","SPECIAL__1","INVENTORY1","COMPARTMEN",
              "COMPARTM_1","FIZ_CD","FOR_MGMT_L","ATTRIBUTIO","PROJECTED_","SOIL_MOIST",
              "SOIL_MOI_1","SOIL_MOI_2","AVAIL_LABE","AVAIL_LA_1","FULL_LABEL","LABEL_CENT",
              "LABEL_CE_1","LABEL_HEIG","LABEL_WIDT","LINE_1_OPE","LINE_1_O_1","LINE_2_POL",
              "LINE_4_CLA","LINE_7_ACT","LINE_7A_ST","PRINTABLE_","SMALL_LABE","OPENING_ID",
              "ORG_UNIT_N","ORG_UNIT_C","ADJUSTED_I","BEC_ZONE_C","BEC_SUBZON","BEC_VARIAN",
              "BEC_PHASE","FREE_TO_GR","NON_FOREST","INTERPRE_1","QUAD_DIAM_","QUAD_DIAM1",
              "QUAD_DIA_1","EST_SITE_I","EST_SITE_1","REFERENCE1","SITE_INDEX","DBH_LIMIT",
              "BASAL_AREA","DATA_SOURC","DATA_SRC_V","VERTICAL_C","SPECIES__1","SPECIES__2",
              "SPECIES__3","SPECIES__4","SPECIES__5","SPECIES__6","SPECIES__7","SPECIES__8",
              "SPECIES__9","SPECIES_10","PROJ_AGE_1","PROJ_AGE_C","PROJ_AGE_2","PROJ_AGE_3",
              "LIVE_VOL_1","LIVE_VOL_2","LIVE_VOL_3","LIVE_VOL_4","LIVE_VOL_5","LIVE_VOL_6",
              "LIVE_VOL_7","LIVE_VOL_8","LIVE_VOL_9","LIVE_VO_10","LIVE_VO_11","LIVE_VO_12",
              "LIVE_VO_13","LIVE_VO_14","LIVE_VO_15","LIVE_VO_16","LIVE_VO_17","DEAD_VOL_1",
              "DEAD_VOL_2","DEAD_VOL_3","DEAD_VOL_4","DEAD_VOL_5","DEAD_VOL_6","DEAD_VOL_7",
              "DEAD_VOL_8","DEAD_VOL_9","DEAD_VO_10","DEAD_VO_11","DEAD_VO_12","DEAD_VO_13",
              "DEAD_VO_14","DEAD_VO_15","DEAD_VO_16","DEAD_VO_17","LIVE_STA_1","LIVE_STA_2",
              "DEAD_STA_1","DEAD_STA_2","WHOLE_STEM","BRANCH_BIO","FOLIAGE_BI","BARK_BIOMA"]

arcpy.management.DeleteField(VRI,dropFields)

#select NE region
arcpy.analysis.Select(region, ""+"studyarea", "OBJECTID_1 = 1")

#study area variable

studyarea = ""+"studyarea"
print(studyarea)

#fix geom of land units
arcpy.RepairGeometry_management(studyarea)
arcpy.RepairGeometry_management(VRI)
print("repaired geom")

#save as new files for faster processing

arcpy.conversion.FeatureClassToFeatureClass(VRI,r"C:\Users\Eli_G\Desktop\project","VRI_clip")


#remove lakes
arcpy.analysis.Erase(studyarea, lakes, "area_nolake")

#reset variable
studyarea = ""+"area_nolake"

#select non vegetation VRI areas and erase
bedrock = "RO"
snowIce = "SI"
expLand = "EL"

whereExpr =  "BCLCS_LE_3 = '%s'" % bedrock + "or BCLCS_LE_3 = '%s'" % snowIce + "or BCLCS_LE_3 = '%s'" % expLand
print(whereExpr)

arcpy.analysis.Select(VRI, "noVegVRI", whereExpr)
arcpy.analysis.Erase(studyarea, "noVegVRI", "veg_area")

#save as shp file
arcpy.conversion.FeatureClassToFeatureClass("veg_area", r"C:\Users\Eli_G\Desktop\project","studyArea_clipped")
print(" file clean up done")

########end of data clean up section
############################################################################
##############################################################################
################# start of project code

import arcpy
import numpy as np
import pandas as pd
import os


##allow overwriting
arcpy.env.overwriteOutput = True

##Create GDB
arcpy.management.CreateFileGDB(r"C:\Users\Eli_G\Desktop\project","project.gdb")

##set workspace
arcpy.env.workspace = r"C:\Users\Eli_G\Desktop\project\project.gdb"

##add fire data to GDB
arcpy.conversion.FeatureClassToFeatureClass(""+"H_FIRE_PLY_polygon.shp","", "fires")
print("fires imported")

#add area files

arcpy.conversion.FeatureClassToFeatureClass("" +"studyArea_clipped.shp","","studyArea")
arcpy.conversion.FeatureClassToFeatureClass(""+"DRPMFFRZNS_polygon.shp", "", "testarea")

print("study area imported")

#variables

Fires = "" + "fires"
studyArea = ""+"studyArea"
zone = ""+"testarea"
print(Fires)
print(studyArea)

arcpy.analysis.Select(zone, "fsjzone", "MFFRZNNM = 'Fort St. John Fire Zone'")

zone = ""+"fsjzone"

arcpy.analysis.Clip(studyArea, zone, ""+"fsjArea")

studyArea = ""+"fsjArea"
print(studyArea)


#list field names for fires
fieldList = arcpy.ListFields(Fires)
for field in fieldList:
    print(field.name)
                       
#set Variables

year = "FIRE_YEAR"
size = "SIZE_HA"
number = "FIRE_NO"
date = "FIRE_DATE"

#clip fires to study area   
arcpy.analysis.Clip(Fires, zone,""+"areaFires", None)
Fires = ""+"areaFires"

#recalculate geom for area
arcpy.management.CalculateGeometryAttributes(Fires,"SIZE_HA AREA", '',"HECTARES", None,"SAME_AS_INPUT")

# reorder date field
arcpy.management.Sort(Fires, "fireSort", [[date,"DESCENDING"]])

Fires = ""+"fireSort"

print(Fires +" sorted")

################################################################   
print("...............starting loops for TSLF ..............")

#array for list of fire files
fireList = [None]


#extract areas with most recent fires in study area
with arcpy.da.SearchCursor(Fires, (year, size, number)) as cursor:
    for i in cursor:
        whereExpr = number +"= '%s'" %i[2] +"And "+ year +"=" + str(i[0])
        print(whereExpr)
        arcpy.analysis.Select(Fires, "f_"+i[2], whereExpr)
        fire = ""+"f_"+i[2]
        arcpy.analysis.Intersect([fire, studyArea], "fire"+str(i[2])+str(i[0]))
        fire = ""+"fire"+str(i[2])+str(i[0])
        print(fire)
        arcpy.management.CalculateGeometryAttributes(fire, "SIZE_HA AREA", '', "HECTARES", None, "SAME_AS_INPUT")
        arcpy.analysis.Erase(zone, fire, "sAreaMinus"+i[2])
        studyArea = ""+"sAreaMinus"+i[2]
        fireList.append("fire"+str(i[2])+str(i[0]))

        
fireList.remove(None)
print(fireList)

#time counter array
time = np.array([[0.00000]*10]*len(fireList))
print(time[0][0])
sizeHa = [0]

#loop to calculate time since fires 
for j in (np.arange(len(fireList))):
    fire = fireList[j]
    print(fire)
    with arcpy.da.SearchCursor(fire, (year, size, number)) as cursor:
        for i in cursor:
            if i[1] == None:
                print(str(i[2])+"null size")
            elif i[0] >= 2017:
                time[j][0] += i[1]
                sizeHa.append(float(i[1]))
            elif i[0] <2017 and i[0]>= 2008:
                time[j][1] += i[1]
                sizeHa.append(float(i[1]))
            elif i[0]<2008 and i[0]>=1993:
                time[j][2] += i[1]
                sizeHa.append(float(i[1]))
            elif i[0] <1993 and i[0]>= 1968:
                time[j][3] += i[1]
                sizeHa.append(float(i[1]))
            elif i[0] <1968 and i[0] >= 1928:
                time[j][4] += i[1]
                sizeHa.append(float(i[1]))
            else:
                time[j][5] += i[1]
                sizeHa.append(float(i[1]))

sizeHa.remove(0)
totBurn = np.sum(sizeHa)
print(totBurn)
time[j][6] = totBurn
aveYear = totBurn/98
print(aveYear)
time[j][7] = aveYear
aveSize = totBurn/len(sizeHa)
print(aveSize)
time[j][8]= aveSize
maxSize = np.amax(sizeHa)
print(maxSize)
time[j][9]= maxSize
  
##Create CSV     
                        
row_lab = fireList
col_lab = ["0-2yrs","2-10yrs","10-25yrs","25-50yrs","50-90yrs",">90yrs",
           "Total HA Burnt","AVE/Year(98)","Ave Size","Max Size"]
df = pd.DataFrame.from_records(time,columns = col_lab, index = row_lab)                    
df.to_csv(""+"All_Units_TSF1.csv")
print("CSV made")


recentFire = [None]
#clean list

#new GDB for outputs
arcpy.management.CreateFileGDB(r"C:\Users\Eli_G\Desktop\project","outputs.gdb")
output = r"C:\Users\Eli_G\Desktop\project\outputs.gdb"

for i in (np.arange(len(fireList))):
    fire = fireList[i]
    with arcpy.da.SearchCursor(fire,(year)) as cursor:
        for j in cursor:
            if j[0] >= 2015:
                print("keeping file")
                recentFire.append(fire)
                arcpy.conversion.FeatureClassToFeatureClass(fire, output, "op_"+fire)
            else:
                print(fire+"removed")
                
recentFire.remove(None)

#########################################################################

print(".................Starting with burn severity...................")


arcpy.conversion.FeatureClassToFeatureClass(""+"BURN_SVRTY_polygon.shp", "","burnSev")
burn = ""+"burnSev"


for i in (np.arange(len(recentFire))):
    fire = fireList[i]
    print(fire)
    arcpy.analysis.Clip(burn, fire,output+"\\"+fire+"Burn",None)
    print("burn clip done" +fire)
    fireBurn = output+"\\"+fire+"Burn"
    arcpy.management.CalculateGeometryAttributes(fireBurn, "AREA_HA AREA", '', "HECTARES", None, "SAME_AS_INPUT")

########## end of project code
##########################################################################
########################################################################
##############################################
############## output clean up

import arcpy
import numpy as np
import pandas as pd
import os


##allow overwriting
arcpy.env.overwriteOutput = True

##set workspace
arcpy.env.workspace = r"C:\Users\Eli_G\Desktop\project\outputs.gdb"


fileList=[None]

FCS = set(arcpy.ListFeatureClasses("*2018Burn") + arcpy.ListFeatureClasses("*2017Burn")+ arcpy.ListFeatureClasses("*2016Burn")+ arcpy.ListFeatureClasses("*2015Burn"))
for i in FCS:
    fileList.append(i)
    
fileList.remove(None)
print(fileList)

arcpy.management.Merge(fileList, r"C:\Users\Eli_G\Desktop\project\BurnSeverity_adj")
arcpy.conversion.FeatureClassToFeatureClass(""+"BurnSeverity_adj", "", "burnSev")

print("merge done")

######### end of output clean up
###############################################################################
###############################################################################
#############################################################################
######## burn severity totals 

import arcpy
import numpy as np
import pandas as pd
import os


##allow overwriting
arcpy.env.overwriteOutput = True

## new GDB
arcpy.management.CreateFileGDB(r"C:\Users\Eli_G\Desktop\project", "analysis.gdb")

##set workspace
arcpy.env.workspace = r"C:\Users\Eli_G\Desktop\project\analysis.gdb"


arcpy.conversion.FeatureClassToFeatureClass(""+"BurnSeverity_adj.shp", "", "burnSev")

#variables

burn = ""+"burnSev"

year = "FIRE_YEAR"
area = "AREA_HA"
rate = "BURN_RATE"

# burn rate [unburned, low, med, high] for years [2015,2016,2017,2018]
counter = np.array([[0.00000000]*5]*4)
print(counter)


#extract sums

with arcpy.da.SearchCursor(burn, (year,rate,area)) as cursor:
    for i in cursor:
        if i[0] == 2015:
            if i[1] == 'Unburned':
                counter[0][0] += float(i[2])
            elif i[1] == 'Low':
                counter[0][1] += float(i[2])
            elif i[1] == 'Medium':
                counter[0][2] += float(i[2])
            elif i[1] == 'High':
                counter[0][3] += float(i[2])
            else:
                counter[0][4] += float(i[2])
        elif i[0] == 2016:
            if i[1] == 'Unburned':
                counter[1][0] += float(i[2])
            elif i[1] == 'Low':
                counter[1][1] += float(i[2])
            elif i[1] == 'Medium':
                counter[1][2] += float(i[2])
            elif i[1] == 'High':
                counter[1][3] += float(i[2])
            else:
                counter[1][4] += float(i[2])
        elif i[0] == 2017:
            if i[1] == 'Unburned':
                counter[2][0] += float(i[2])
            elif i[1] == 'Low':
                counter[2][1] += float(i[2])
            elif i[1] == 'Medium':
                counter[2][2] += float(i[2])
            elif i[1] == 'High':
                counter[2][3] += float(i[2])
            else:
                counter[2][4] += float(i[2])
        else:         
            if i[1] == 'Unburned':
                counter[3][0] += float(i[2])
            elif i[1] == 'Low':
                counter[3][1] += float(i[2])
            elif i[1] == 'Medium':
                counter[3][2] += float(i[2])
            elif i[1] == 'High':
                counter[3][3] += float(i[2])
            else:
                counter[3][4] += float(i[2])

        
        
        
print(counter)

##Create CSV     
                        
row_lab = ["2015","2016","2017","2018"]
col_lab = ['Unburned', 'Low','Medium','High','Unknown']
df = pd.DataFrame.from_records(counter,columns = col_lab, index = row_lab)                    
df.to_csv(""+"Burn_Severity.csv")
print("CSV made")

