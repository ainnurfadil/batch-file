import importlib
import sys
import platform
import collections
import traceback

from types import ModuleType
from typing import Dict, List, Optional, Union

from qtpy import QtWidgets, QtCore

import bpy


class LaunchQtApp(bpy.types.Operator):
    """A Base class for operators to launch a Qt app."""

    _window = Union[QtWidgets.QDialog, ModuleType]
    _init_args: Optional[List] = list()
    _init_kwargs: Optional[Dict] = dict()
    bl_idname: str = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.bl_idname is None:
            raise NotImplementedError("Attribute `bl_idname` must be set!")

        GlobalClass.app = BlenderApplication.get_app()

    def execute(self, context):
        """Execute the operator.

        The child class must implement `execute()` where it only has to set
        `self._window` to the desired Qt window and then simply run
        `return super().execute(context)`.
        `self._window` is expected to have a `show` method.
        If the `show` method requires arguments, you can set `self._show_args`
        and `self._show_kwargs`. `args` should be a list, `kwargs` a
        dictionary.
        """

        # Check if there's already a valid window stored for this operator
        existing_window = BlenderApplication.get_window(self.bl_idname)
        if existing_window and self._is_window_valid(existing_window):
            # Use existing window if available and valid
            window_to_use = existing_window
        else:
            # Create new window using the class-defined _window
            if isinstance(self._window, type):
                # If _window is a class, instantiate it
                window_to_use = self._window(
                    *self._init_args, **self._init_kwargs)
            else:
                # If _window is already an instance or module, use it directly
                window_to_use = self._window

            # Store the new window
            BlenderApplication.store_window(self.bl_idname, window_to_use)

        if not isinstance(window_to_use, (QtWidgets.QWidget, ModuleType)):
            raise AttributeError(
                "`window` should be a `QWidget or module`. Got: {}".format(
                    str(type(window_to_use))
                )
            )

        def pull_to_front(window):
            """Pull window forward to screen.

            If Window is minimized this will un-minimize, then it can be raised
            and activated to the front.
            """
            window.setWindowState(
                (window.windowState() & ~
                 QtCore.Qt.WindowMinimized) | QtCore.Qt.WindowActive
            )
            window.raise_()
            window.activateWindow()

        if isinstance(window_to_use, ModuleType):
            window_to_use.show()

            # Pull window to the front
            actual_window = None
            if hasattr(window_to_use, "window"):
                actual_window = window_to_use.window
            elif hasattr(window_to_use, "_window"):
                actual_window = window_to_use._window

            if actual_window:
                pull_to_front(actual_window)

        else:
            if not window_to_use.isVisible():
                origin_flags = window_to_use.windowFlags()
                on_top_flags = origin_flags | QtCore.Qt.WindowStaysOnTopHint
                window_to_use.setWindowFlags(on_top_flags)
                window_to_use.show()

            pull_to_front(window_to_use)

        return {'FINISHED'}

    def _is_window_valid(self, window):
        """Check if a window is still valid and accessible."""
        try:
            if isinstance(window, ModuleType):
                # For module windows, check if they have a valid window attribute
                actual_window = None
                if hasattr(window, "window"):
                    actual_window = window.window
                elif hasattr(window, "_window"):
                    actual_window = window._window

                if actual_window:
                    # Check if the actual window is still valid
                    return not actual_window.isHidden() and actual_window.isVisible() is not None
                return True
            else:
                # For QWidget windows, check if they're still valid
                return (hasattr(window, 'isVisible') and
                        window.isVisible() is not None and
                        not window.isHidden())
        except (RuntimeError, AttributeError):
            # Window has been deleted or is no longer accessible
            return False


class GlobalClass:
    app = None
    main_thread_callbacks = collections.deque()
    is_windows = platform.system().lower() == "windows"


class BlenderApplication:
    _instance = None
    blender_windows = {}

    @classmethod
    def get_app(cls):
        if cls._instance is None:
            application = QtWidgets.QApplication.instance()
            if application is None:
                application = QtWidgets.QApplication(sys.argv)

            cls._prepare_qapplication(application)
            cls._instance = application

        return cls._instance

    @classmethod
    def _prepare_qapplication(cls, application: QtWidgets.QApplication):
        application.setQuitOnLastWindowClosed(False)
        application.lastWindowClosed.connect(cls.reset)

    @classmethod
    def reset(cls):
        cls._instance = None

    @classmethod
    def store_window(cls, identifier, window):
        """Store a window reference, cleaning up old ones if needed."""
        current_window = cls.get_window(identifier)

        # Only close if it's a different window and still valid
        if current_window and current_window != window:
            try:
                if isinstance(current_window, QtWidgets.QWidget):
                    if current_window.isVisible():
                        current_window.close()
                elif isinstance(current_window, ModuleType):
                    # For module windows, try to close the actual window
                    actual_window = None
                    if hasattr(current_window, "window"):
                        actual_window = current_window.window
                    elif hasattr(current_window, "_window"):
                        actual_window = current_window._window

                    if actual_window and hasattr(actual_window, 'close'):
                        actual_window.close()
            except (RuntimeError, AttributeError):
                # Window was already deleted, ignore
                pass

        cls.blender_windows[identifier] = window

    @classmethod
    def get_window(cls, identifier):
        """Get a stored window, removing invalid references."""
        window = cls.blender_windows.get(identifier)

        if window:
            try:
                # Check if window is still valid
                if isinstance(window, QtWidgets.QWidget):
                    # Try to access a property to see if widget is still valid
                    _ = window.isVisible()
                elif isinstance(window, ModuleType):
                    # For modules, check if they still have valid window attributes
                    if hasattr(window, "window"):
                        _ = window.window.isVisible() if window.window else None
                    elif hasattr(window, "_window"):
                        _ = window._window.isVisible() if window._window else None

                return window
            except (RuntimeError, AttributeError):
                # Window is no longer valid, remove it
                cls.blender_windows.pop(identifier, None)
                return None

        return None


"""
Tool Manager for Blender Acacia Tools
Provides automatic discovery and registration of tools
"""


class ToolManager:
    """Manages discovery and registration of Blender tools"""

    def __init__(self):
        self.registered_tools = {}
        self.tool_modules = []

    def discover_tools(self, tool_paths):
        """
        Discover tools from given module paths

        Args:
            tool_paths: List of module paths to search for tools

        Returns:
            List of tool definitions
        """
        discovered_tools = []

        for tool_path in tool_paths:
            try:
                # Import the tool module
                module = importlib.import_module(tool_path)

                if not hasattr(module, 'TOOL_DEFINITION'):
                    print(
                        f"Tool module {tool_path} has no get_tool_definition function")
                    continue

                tool_def = module.TOOL_DEFINITION.copy()
                tool_def['module'] = module
                tool_def['module_path'] = tool_path
                discovered_tools.append(tool_def)

            except Exception as e:
                print(f"Error discovering tool from {tool_path}: {e}")
                traceback.print_exc()
        return discovered_tools

    def register_tools(self, tools):
        """
        Register discovered tools

        Args:
            tools: List of tool definitions to register
        """
        for tool in tools:
            try:
                module = tool['module']

                if not hasattr(module, 'register'):
                    print(f"Tool {tool['name']} has no register function")
                    continue

                module.register()
                self.registered_tools[tool['name']] = tool

            except Exception as e:
                print(
                    f"Error registering tool {tool.get('name', 'Unknown')}: {e}")
                traceback.print_exc()

    def unregister_tools(self):
        """Unregister all registered tools"""
        for tool_name, tool in self.registered_tools.items():
            try:
                module = tool['module']

                if not hasattr(module, 'unregister'):
                    print(f"Tool {tool_name} has no unregister function")
                    continue

                module.unregister()
                print(f"Unregistered tool: {tool_name}")

            except Exception as e:
                print(f"Error unregistering tool {tool_name}: {e}")
                traceback.print_exc()

        self.registered_tools.clear()

    def get_registered_tools(self):
        """Get all registered tools"""
        return self.registered_tools.copy()

    def get_tools_by_category(self, category):
        """Get tools filtered by category"""
        return [
            tool for tool in self.registered_tools.values()
            if tool.get('category') == category
        ]


# Global tool manager instance
tool_manager = ToolManager()


def discover_and_register_tools(tool_paths):
    """
    Convenience function to discover and register tools

    Args:
        tool_paths: List of module paths to search for tools
    """
    tools = tool_manager.discover_tools(tool_paths)
    tool_manager.register_tools(tools)


def unregister_all_tools():
    """Convenience function to unregister all tools"""
    tool_manager.unregister_tools()


def get_menu_items():
    """Get menu items for all registered tools"""
    menu_items = []

    for tool in tool_manager.get_registered_tools().values():
        if 'operator' not in tool:
            continue

        menu_items.append({
            'label': tool['name'],
            'operator_id': tool['operator'].bl_idname,
            'description': tool.get('description', ''),
            'category': tool.get('category', 'General'),
            'icon': tool.get('icon', None)
        })

    return menu_items
