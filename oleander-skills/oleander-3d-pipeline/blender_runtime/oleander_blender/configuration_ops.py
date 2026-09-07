import json
import bpy

from .configuration import capture_configuration, configuration_names, restore_configuration


class OLEANDER_OT_save_configuration(bpy.types.Operator):
    bl_idname = "oleander.save_configuration"
    bl_label = "Save Configuration"
    bl_description = "Capture transform, visibility and governed parameter metadata by OLE ID without duplicating the master model."
    bl_options = {"REGISTER", "UNDO"}

    name: bpy.props.StringProperty(name="Configuration", default="NORMAL")

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

    def execute(self, context):
        try:
            config = capture_configuration(context.scene, self.name)
        except ValueError as exc:
            self.report({"ERROR"}, str(exc))
            return {"CANCELLED"}
        self.report({"INFO"}, f"Saved configuration {self.name}: {len(config['objects'])} object(s)")
        return {"FINISHED"}


class OLEANDER_OT_restore_configuration(bpy.types.Operator):
    bl_idname = "oleander.restore_configuration"
    bl_label = "Restore Configuration"
    bl_description = "Restore a captured OLE configuration by stable object identity."
    bl_options = {"REGISTER", "UNDO"}

    name: bpy.props.StringProperty(name="Configuration", default="NORMAL")

    def invoke(self, context, event):
        names = configuration_names(context.scene)
        if names:
            self.name = names[0]
        return context.window_manager.invoke_props_dialog(self)

    def execute(self, context):
        try:
            result = restore_configuration(context.scene, self.name)
        except KeyError:
            self.report({"ERROR"}, f"Unknown configuration: {self.name}")
            return {"CANCELLED"}
        self.report({"INFO"}, f"Restored {len(result['restored'])} object(s); missing: {len(result['missing'])}")
        return {"FINISHED"}


class OLEANDER_OT_list_configurations(bpy.types.Operator):
    bl_idname = "oleander.list_configurations"
    bl_label = "List Configurations"
    bl_description = "Write saved configuration names to an inspectable Text datablock."

    def execute(self, context):
        payload = {"schema": "OLEANDER_CONFIGURATION_INDEX_v0.1", "names": configuration_names(context.scene)}
        text = bpy.data.texts.get("OLEANDER_CONFIGURATIONS.json") or bpy.data.texts.new("OLEANDER_CONFIGURATIONS.json")
        text.clear()
        text.write(json.dumps(payload, indent=2, ensure_ascii=False))
        self.report({"INFO"}, f"Configurations: {len(payload['names'])}")
        return {"FINISHED"}


CLASSES = (
    OLEANDER_OT_save_configuration,
    OLEANDER_OT_restore_configuration,
    OLEANDER_OT_list_configurations,
)
