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
    QgsLayoutItemLegend,
    QgsLayoutItemScaleBar,
    QgsLayoutExporter,
    QgsLayoutPoint,
    QgsLayoutSize,
    QgsUnitTypes,
    QgsMarkerSymbol,
    QgsSingleSymbolRenderer,
)
from qgis.PyQt.QtGui import QColor, QFont

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "outputs"
OUT.mkdir(exist_ok=True)

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

        # Grayscale continuous ramp: restrained, readable, and independent of a categorical interpretation.
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

        symbol = QgsMarkerSymbol.createSimple({
            "name":"circle", "color":"255,255,255", "outline_color":"0,0,0",
            "outline_width":"0.45", "size":"2.6"
        })
        points.setRenderer(QgsSingleSymbolRenderer(symbol))

        project.addMapLayer(raster)
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
        subtitle.setText("SYNTHETIC TRAINING DATA | EPSG:3857 runtime placeholder | Quartic kernel | raw density")
        subtitle.setFont(QFont("DejaVu Sans", 9))
        subtitle.adjustSizeToText()
        subtitle.attemptMove(QgsLayoutPoint(15, 21, QgsUnitTypes.LayoutMillimeters))
        layout.addLayoutItem(subtitle)

        map_item = QgsLayoutItemMap(layout)
        map_item.attemptMove(QgsLayoutPoint(15, 34, QgsUnitTypes.LayoutMillimeters))
        map_item.attemptResize(QgsLayoutSize(300, 245, QgsUnitTypes.LayoutMillimeters))
        map_item.setExtent(raster.extent())
        map_item.setLayers([points, raster])
        map_item.setFrameEnabled(True)
        layout.addLayoutItem(map_item)

        legend = QgsLayoutItemLegend(layout)
        legend.setTitle("Layers / density ramp")
        legend.setLinkedMap(map_item)
        legend.attemptMove(QgsLayoutPoint(322, 45, QgsUnitTypes.LayoutMillimeters))
        legend.attemptResize(QgsLayoutSize(83, 70, QgsUnitTypes.LayoutMillimeters))
        layout.addLayoutItem(legend)

        scale = QgsLayoutItemScaleBar(layout)
        scale.setStyle("Single Box")
        scale.setLinkedMap(map_item)
        scale.setUnits(QgsUnitTypes.DistanceMeters)
        scale.setNumberOfSegments(4)
        scale.setNumberOfSegmentsLeft(0)
        scale.setUnitsPerSegment(100)
        scale.setUnitLabel("m")
        scale.attemptMove(QgsLayoutPoint(322, 128, QgsUnitTypes.LayoutMillimeters))
        scale.attemptResize(QgsLayoutSize(78, 16, QgsUnitTypes.LayoutMillimeters))
        layout.addLayoutItem(scale)

        note = QgsLayoutItemLabel(layout)
        note.setText(
            "Reality status\n"
            "QGIS runtime: VERIFIED\n"
            "Project CRS: OPEN\n"
            "Project data: OPEN\n\n"
            "North arrow intentionally omitted:\n"
            "the XY plane is synthetic and has\n"
            "no asserted geographic orientation."
        )
        note.setFont(QFont("DejaVu Sans", 9))
        note.attemptMove(QgsLayoutPoint(322, 158, QgsUnitTypes.LayoutMillimeters))
        note.attemptResize(QgsLayoutSize(83, 65, QgsUnitTypes.LayoutMillimeters))
        layout.addLayoutItem(note)

        footer = QgsLayoutItemLabel(layout)
        footer.setText("Observed pattern only. Bandwidth/pixel sensitivity and edge spill must be read with the metrics register; no project conclusion is claimed.")
        footer.setFont(QFont("DejaVu Sans", 8))
        footer.attemptMove(QgsLayoutPoint(322, 235, QgsUnitTypes.LayoutMillimeters))
        footer.attemptResize(QgsLayoutSize(83, 38, QgsUnitTypes.LayoutMillimeters))
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
            "extent": [raster.extent().xMinimum(), raster.extent().yMinimum(), raster.extent().xMaximum(), raster.extent().yMaximum()],
            "north_arrow": "INTENTIONALLY_OMITTED_SYNTHETIC_ORIENTATION",
            "scale_bar": "100 m x 4 segments",
            "crs": "EPSG:3857_RUNTIME_PLACEHOLDER",
        })
finally:
    qgs.exitQgis()

(OUT / "qgis_layout_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
print(json.dumps(manifest, indent=2))
