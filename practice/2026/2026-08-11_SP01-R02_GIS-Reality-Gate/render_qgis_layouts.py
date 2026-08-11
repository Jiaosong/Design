from pathlib import Path
import json

from qgis.core import (
    QgsApplication,
    QgsProject,
    QgsVectorLayer,
    QgsRasterLayer,
    QgsCoordinateReferenceSystem,
    QgsRasterShader,
    QgsColorRampShader,
    QgsSingleBandPseudoColorRenderer,
    QgsPrintLayout,
    QgsLayoutItemMap,
    QgsLayoutItemLabel,
    QgsLayoutItemScaleBar,
    QgsLayoutExporter,
    QgsLayoutPoint,
    QgsLayoutSize,
    QgsUnitTypes,
    QgsMarkerSymbol,
    QgsSingleSymbolRenderer,
    QgsFillSymbol,
    QgsFeature,
    QgsGeometry,
    QgsPointXY,
    QgsRectangle,
)
from qgis.PyQt.QtGui import QColor, QFont

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "outputs"
OUT.mkdir(exist_ok=True)

# Common extent is deliberately fixed across all bandwidth sheets so visual comparison
# does not accidentally change map scale. It also contains the largest KDE spill extent.
COMMON_EXTENT = QgsRectangle(-150.0, -150.0, 1200.0, 1200.0)
STUDY_RING = [
    QgsPointXY(0, 0), QgsPointXY(1000, 0), QgsPointXY(1000, 1000),
    QgsPointXY(0, 1000), QgsPointXY(0, 0)
]

QgsApplication.setPrefixPath("/usr", True)
qgs = QgsApplication([], False)
qgs.initQgis()

manifest = []
try:
    for radius in (75, 150, 300):
        project = QgsProject.instance()
        project.clear()
        project.setCrs(QgsCoordinateReferenceSystem("EPSG:3857"))

        points = QgsVectorLayer(str(OUT / "training_points.gpkg") + "|layername=training_points", "24 synthetic training points", "ogr")
        raster = QgsRasterLayer(str(OUT / f"kde_r{radius}_p25.tif"), f"KDE raw | r={radius} m | p=25 m")
        if not points.isValid() or not raster.isValid():
            raise RuntimeError(f"Invalid QGIS layer(s) for radius {radius}")

        # Each bandwidth is stretched to its own observed min/max to compare morphology.
        # Therefore shade must NOT be read as a common absolute-density scale across sheets.
        stats = raster.dataProvider().bandStatistics(1)
        shader = QgsRasterShader()
        ramp = QgsColorRampShader()
        ramp.setColorRampType(QgsColorRampShader.Interpolated)
        ramp.setColorRampItemList([
            QgsColorRampShader.ColorRampItem(stats.minimumValue, QColor(255,255,255), "low"),
            QgsColorRampShader.ColorRampItem(stats.maximumValue, QColor(20,20,20), "high"),
        ])
        shader.setRasterShaderFunction(ramp)
        raster.setRenderer(QgsSingleBandPseudoColorRenderer(raster.dataProvider(), 1, shader))

        point_symbol = QgsMarkerSymbol.createSimple({
            "name":"circle", "color":"255,255,255", "outline_color":"0,0,0",
            "outline_width":"0.45", "size":"2.6"
        })
        points.setRenderer(QgsSingleSymbolRenderer(point_symbol))

        study = QgsVectorLayer("Polygon?crs=EPSG:3857", "exercise study boundary 0-1000 m", "memory")
        feat = QgsFeature()
        feat.setGeometry(QgsGeometry.fromPolygonXY([STUDY_RING]))
        study.dataProvider().addFeature(feat)
        study.updateExtents()
        study_symbol = QgsFillSymbol.createSimple({
            "color":"255,255,255,0", "outline_color":"0,0,0,255",
            "outline_width":"0.55", "outline_style":"dash"
        })
        study.setRenderer(QgsSingleSymbolRenderer(study_symbol))

        project.addMapLayer(raster)
        project.addMapLayer(study)
        project.addMapLayer(points)

        layout = QgsPrintLayout(project)
        layout.initializeDefaults()
        layout.setName(f"SP01_R02_r{radius}")
        page = layout.pageCollection().page(0)
        page.setPageSize(QgsLayoutSize(420, 297, QgsUnitTypes.LayoutMillimeters))

        title = QgsLayoutItemLabel(layout)
        title.setText(f"SP01-R02 | QGIS KDE Reality Gate | radius {radius} m | pixel 25 m")
        title.setFont(QFont("DejaVu Sans", 16))
        title.adjustSizeToText()
        title.attemptMove(QgsLayoutPoint(15, 10, QgsUnitTypes.LayoutMillimeters))
        layout.addLayoutItem(title)

        subtitle = QgsLayoutItemLabel(layout)
        subtitle.setText("SYNTHETIC TRAINING DATA | EPSG:3857 runtime placeholder | Quartic kernel | raw KDE | COMMON MAP EXTENT")
        subtitle.setFont(QFont("DejaVu Sans", 9))
        subtitle.adjustSizeToText()
        subtitle.attemptMove(QgsLayoutPoint(15, 21, QgsUnitTypes.LayoutMillimeters))
        layout.addLayoutItem(subtitle)

        # Square map frame + fixed common extent = identical map scale across all three sheets.
        map_item = QgsLayoutItemMap(layout)
        map_item.attemptMove(QgsLayoutPoint(15, 34, QgsUnitTypes.LayoutMillimeters))
        map_item.attemptResize(QgsLayoutSize(245, 245, QgsUnitTypes.LayoutMillimeters))
        map_item.setExtent(COMMON_EXTENT)
        map_item.setLayers([points, study, raster])
        map_item.setFrameEnabled(True)
        layout.addLayoutItem(map_item)

        key = QgsLayoutItemLabel(layout)
        key.setText(
            "MAP KEY / COMPARISON RULE\n"
            "○  synthetic training point\n"
            "--  0–1000 m exercise study boundary\n\n"
            "KDE shade (per-sheet stretch)\n"
            "dark = higher raw KDE\n"
            "light = lower raw KDE\n"
            "Do NOT compare shade as an absolute\n"
            "density value between bandwidth sheets."
        )
        key.setFont(QFont("DejaVu Sans", 9))
        key.attemptMove(QgsLayoutPoint(270, 43, QgsUnitTypes.LayoutMillimeters))
        key.attemptResize(QgsLayoutSize(135, 70, QgsUnitTypes.LayoutMillimeters))
        layout.addLayoutItem(key)

        scale = QgsLayoutItemScaleBar(layout)
        scale.setStyle("Single Box")
        scale.setLinkedMap(map_item)
        scale.setUnits(QgsUnitTypes.DistanceMeters)
        scale.setNumberOfSegments(3)
        scale.setNumberOfSegmentsLeft(0)
        scale.setUnitsPerSegment(100)
        scale.setUnitLabel("m")
        scale.attemptMove(QgsLayoutPoint(270, 122, QgsUnitTypes.LayoutMillimeters))
        layout.addLayoutItem(scale)

        note = QgsLayoutItemLabel(layout)
        note.setText(
            "REALITY STATUS\n"
            "QGIS runtime: VERIFIED\n"
            "Project CRS: OPEN\n"
            "Project data: OPEN\n\n"
            "North arrow intentionally omitted:\n"
            "the XY plane is synthetic and has\n"
            "no asserted geographic orientation."
        )
        note.setFont(QFont("DejaVu Sans", 9))
        note.attemptMove(QgsLayoutPoint(270, 157, QgsUnitTypes.LayoutMillimeters))
        note.attemptResize(QgsLayoutSize(135, 58, QgsUnitTypes.LayoutMillimeters))
        layout.addLayoutItem(note)

        footer = QgsLayoutItemLabel(layout)
        footer.setText(
            "EDGE / SENSITIVITY NOTE\n"
            "Raster spill outside the dashed study box is measured in edge_effect_metrics.csv.\n"
            "Pixel-size sensitivity is measured at 10 / 25 / 50 m.\n"
            "Observed pattern only; no real-site or project conclusion is claimed."
        )
        footer.setFont(QFont("DejaVu Sans", 8))
        footer.attemptMove(QgsLayoutPoint(270, 224, QgsUnitTypes.LayoutMillimeters))
        footer.attemptResize(QgsLayoutSize(135, 48, QgsUnitTypes.LayoutMillimeters))
        layout.addLayoutItem(footer)

        out_png = OUT / f"QGIS_LAYOUT_r{radius}_p25.png"
        settings = QgsLayoutExporter.ImageExportSettings()
        settings.dpi = 160
        result = QgsLayoutExporter(layout).exportToImage(str(out_png), settings)
        if result != QgsLayoutExporter.Success or not out_png.exists() or out_png.stat().st_size == 0:
            raise RuntimeError(f"QGIS layout export failed for radius {radius}: {result}")

        manifest.append({
            "radius_m": radius,
            "pixel_m": 25,
            "png": out_png.name,
            "bytes": out_png.stat().st_size,
            "raster_extent": [raster.extent().xMinimum(), raster.extent().yMinimum(), raster.extent().xMaximum(), raster.extent().yMaximum()],
            "common_map_extent": [COMMON_EXTENT.xMinimum(), COMMON_EXTENT.yMinimum(), COMMON_EXTENT.xMaximum(), COMMON_EXTENT.yMaximum()],
            "map_scale": map_item.scale(),
            "study_boundary": [0,0,1000,1000],
            "density_rendering":"PER_SHEET_MIN_MAX_STRETCH_FOR_MORPHOLOGY_ONLY",
            "north_arrow":"INTENTIONALLY_OMITTED_SYNTHETIC_ORIENTATION",
            "scale_bar":"100 m x 3 segments",
            "crs":"EPSG:3857_RUNTIME_PLACEHOLDER",
        })
finally:
    qgs.exitQgis()

(OUT / "qgis_layout_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
print(json.dumps(manifest, indent=2))
