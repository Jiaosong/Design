# Run inside QGIS. NOT RUN in the automation runtime.
# Replace the placeholder CRS with a suitable projected CRS for real project work.
import processing
from qgis.core import QgsVectorLayer, QgsProject

uri = "file:///training_points.csv?delimiter=,&xField=x_m&yField=y_m&crs=EPSG:3857"
points = QgsVectorLayer(uri, "training_points", "delimitedtext")
QgsProject.instance().addMapLayer(points)

for radius in (75, 150, 300):
    processing.run("qgis:heatmapkerneldensityestimation", {
        "INPUT": points,
        "RADIUS": radius,
        "PIXEL_SIZE": 25,
        "WEIGHT_FIELD": "weight",
        "KERNEL": 0,
        "DECAY": 0,
        "OUTPUT_VALUE": 0,
        "OUTPUT": f"qgis_kde_{radius}m.tif"
    })
