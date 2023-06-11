import arcpy
from arcpy.sa import *

arcpy.env.overwriteOutput = True

in_surface_raster = arcpy.GetParameterAsText(0)
out_raster_path = arcpy.GetParameterAsText(1)
pour_point_data = arcpy.GetParameterAsText(2)
flow_accumulation_raster = arcpy.GetParameter(3)
raster_to_polygon = arcpy.GetParameter(4)
z_limit = arcpy.GetParameterAsText(5)
pour_point_field = arcpy.GetParameterAsText(5)
flow_direction_type = arcpy.GetParameterAsText(7)
out_drop_raster = arcpy.GetParameterAsText(8)


fill_raster = Fill(in_surface_raster, z_limit)

flow_direction_raster = FlowDirection(fill_raster, out_drop_raster, flow_direction_type)

if pour_point_data == "":
    out_raster = Basin(flow_direction_raster)
else:
    out_raster = Watershed(flow_direction_raster, pour_point_data, pour_point_field)

if flow_accumulation_raster:
    flow_accu_raster = FlowAccumulation(flow_direction_raster, flow_direction_type)
    flow_accu_raster.save(r"{}_accu".format(out_raster_path))

if raster_to_polygon:
    arcpy.conversion.RasterToPolygon(out_raster, r"{}_polygon".format(out_raster_path))
else:
    out_raster.save(r"{}".format(out_raster_path))

    
