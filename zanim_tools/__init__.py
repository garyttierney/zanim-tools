# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTIBILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
import bpy

from zanim_tools.operators.armature_from_mouse import ArmatureFromMouse

bl_info = {
    "name": "zanim_tools",
    "author": "Gary Tierney",
    "description": "",
    "blender": (2, 80, 0),
    "version": (0, 0, 1),
    "location": "",
    "warning": "",
    "category": "Generic"
}


def menu_func(self, context):
    self.layout.operator(ArmatureFromMouse.bl_idname, text="Create armature from mouse points")


# Register and add to the "view" menu (required to also use F3 search "Raycast View Modal Operator" for quick access)
def register():
    bpy.utils.register_class(ArmatureFromMouse)
    bpy.types.VIEW3D_MT_edit_armature.append(menu_func)


def unregister():
    bpy.utils.unregister_class(ArmatureFromMouse)
    bpy.types.VIEW3D_MT_edit_armature.remove(menu_func)
