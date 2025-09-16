from typing import Dict

import bpy
import bpy.utils.previews

from .ops import (
    BlenderApplication,
    discover_and_register_tools,
    unregister_all_tools,
    get_menu_items
)

PREVIEW_COLLECTIONS: Dict = dict()

# List of tool module paths to discover
TOOL_MODULES = [
    "Acacia.hosts.Blender.Scripts.Asset.modelling_tool.app",
    "Acacia.hosts.Blender.Scripts.Animation.animation_tool.app",
    # Add more tool modules here as needed
]


class TOPBAR_MT_lmn(bpy.types.Menu):
    """LMN Tools menu."""

    bl_idname = "TOPBAR_MT_lmn"
    bl_label = "LMN"

    def draw(self, context):
        """Draw the menu in the UI."""
        layout = self.layout

        # Get menu items from tool manager
        menu_items = get_menu_items()

        if not menu_items:
            layout.label(text="No tools available")
            return

        # Group items by category
        categories = {}
        for item in menu_items:
            category = item.get('category', 'General')
            if category not in categories:
                categories[category] = []
            categories[category].append(item)

        # Draw menu items grouped by category
        for category, items in categories.items():

            if len(categories) > 1:
                layout.label(text=category)

            for item in items:
                layout.operator(item['operator_id'], text=item['label'])

            if len(categories) > 1:  # Add separator between categories
                layout.separator()


def draw_LMN_menu(self, context):
    """Draw the LMN menu in the top bar."""
    self.layout.menu(TOPBAR_MT_lmn.bl_idname)


classes = [
    TOPBAR_MT_lmn
]


def register():
    """Register the operators and menu."""
    pcoll = bpy.utils.previews.new()
    PREVIEW_COLLECTIONS["lmn"] = pcoll

    BlenderApplication.get_app()

    # Discover and register all tools automatically
    discover_and_register_tools(TOOL_MODULES)

    # Register menu classes
    for cls in classes:
        bpy.utils.register_class(cls)

    bpy.types.TOPBAR_MT_editor_menus.append(draw_LMN_menu)

    print("LMN Menu System: Loaded successfully.")


def unregister():
    """Unregister the operators and menu."""
    # Remove menu from top bar
    bpy.types.TOPBAR_MT_editor_menus.remove(draw_LMN_menu)

    # Unregister menu classes
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

    # Unregister all tools
    unregister_all_tools()

    # Clean up preview collections
    pcoll = PREVIEW_COLLECTIONS.pop("lmn", None)
    if pcoll:
        bpy.utils.previews.remove(pcoll)

    print("LMN Menu System: Unloaded successfully.")
