from pathlib import Path
from qgis.core import (
    QgsApplication,
    QgsProject,
    QgsVectorLayer,
    QgsRasterLayer,
    QgsCoordinateReferenceSystem,
    Qgis,
)

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "outputs"
OUT.mkdir(exist_ok=True)

QgsApplication.setPrefixPath("/usr", True)
qgs = QgsApplication([], False)
qgs.initQgis()

try:
    project = QgsProject.instance()
    project.clear()
    project.setCrs(QgsCoordinateReferenceSystem("EPSG:3857"))
    project.setCustomVariables({
        "OLEANDER_PRACTICE": "SP01-R02 GIS Reality Gate",
        "OLEANDER_TRUTH_STATE": "TRAINING_SYNTHETIC",
        "QGIS_RUNTIME_GATE": "EXECUTED",
        "PROJECT_CRS_GATE": "OPEN",
        "PROJECT_DATA_GATE": "OPEN",
        "CRS_NOTE": "EPSG:3857 is an exercise/runtime placeholder, not an approved project CRS",
    })

    gpkg = OUT / "training_points.gpkg"
    points = QgsVectorLayer(f"{gpkg}|layername=training_points", "training_points_SYNTHETIC", "ogr")
    if not points.isValid():
        raise RuntimeError(f"Invalid point layer: {gpkg}")
    project.addMapLayer(points)

    for radius in (75, 150, 300):
        tif = OUT / f"kde_r{radius}_p25.tif"
        lyr = QgsRasterLayer(str(tif), f"KDE_r{radius}m_p25m_EXERCISE")
        if not lyr.isValid():
            raise RuntimeError(f"Invalid raster layer: {tif}")
        project.addMapLayer(lyr)

    qgz = OUT / "SP01_R02_QGIS_Runtime.qgz"
    if not project.write(str(qgz)):
        raise RuntimeError(f"Failed to write QGIS project: {qgz}")

    (OUT / "pyqgis_version.txt").write_text(Qgis.QGIS_VERSION, encoding="utf-8")
    print(f"QGIS_VERSION={Qgis.QGIS_VERSION}")
    print(f"QGZ={qgz}")
finally:
    qgs.exitQgis()
