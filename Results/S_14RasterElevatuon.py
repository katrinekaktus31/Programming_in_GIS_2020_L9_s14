import arcpy
arcpy.env.overwriteOutput = True
inputFc = arcpy.GetParameterAsText(0)
rasterElevation = arcpy.GetParameterAsText(1)
resultFile = arcpy.GetParameterAsText(2)
newFields = arcpy.GetParameterAsText(3)

arcpy.CopyFeatures_management(inputFc, resultFile)
arcpy.AddMessage("New shape file was created")

if arcpy.Describe(inputFc).spatialReference.name == arcpy.Describe(rasterElevation).spatialReference.name:
    arcpy.AddMessage("Coordinate systems are valid")
else:
     arcpy.AddMessage("Coordinate systems are invalid.")
     sr_name = arcpy.Describe(rasterElevation).spatialReference.name
     arcpy.Project_management(resultFile, resultFile, sr_name)
     arcpy.AddMessage("Coordinate systems was reprojected")

# determine the value of heights in the specified coordinates
vertexHeight = []
with arcpy.da.SearchCursor(resultFile, ["SHAPE@XY",]) as cursor:
    for row in cursor:
        x, y = row[0]
        result = arcpy.GetCellValue_management(rasterElevation, str(row[0][0])+' '+str(row[0][1]))
        vertexHeight.append(result.getOutput(0))
arcpy.AddMessage("The values of heights was defined")

arcpy.AddField_management(resultFile, newFields, "SHORT")

with arcpy.da.UpdateCursor(resultFile, newFields) as cursor:
    for row in cursor:
        i = 0
        row[0] = vertexHeight[i]
        cursor.updateRow(row)
        i+=1

arcpy.AddMessage("New feild " + newFields+ "was created.")
arcpy.AddMessage("All done!")

