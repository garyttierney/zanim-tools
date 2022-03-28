import blf
import bpy
from bpy.types import Armature, EditBone
from gpu_extras.presets import draw_circle_2d

from ..utils.raycast import cast_ray, cast_ray_at
from ..utils.screen import screen_to_world_ray


def ui(self, context):
    font_id = 0  # XXX, need to find out how best to get this.

    blf.color(0, 1.0, 1.0, 1.0, 1.0)
    blf.size(font_id, 12, 72)
    blf.position(font_id, 15, 42, 0)
    blf.draw(font_id, "CTRL+click to complete chain")
    blf.position(font_id, 15, 28, 0)
    blf.draw(font_id, "SHIFT+LMB to place bone using vertex normals for ray casts")
    blf.position(font_id, 15, 14, 0)
    blf.draw(font_id, "SHIFT+LMB to place bone using screen space direction for ray casts")

    draw_circle_2d(self.mouse_pos, (1, 1, 1, 1), 16.0, segments=32)
    draw_circle_2d(self.mouse_pos, (0, 0, 0, 1), 4.0, segments=32)


class ArmatureFromMouse(bpy.types.Operator):
    bl_idname = "view3d.armature_from_mouse"
    bl_label = "Armature From Mouse Operator"

    def __init__(self):
        self._handle = None
        self.mouse_pos = (0, 0)
        self.last_bone = None  # type:  EditBone

    def main(self, context: bpy.types.Context, event, complete_chain=False, use_normals=False):
        """Run this function on left mouse, execute the ray cast"""
        origin, direction = screen_to_world_ray(context, event.mouse_region_x, event.mouse_region_y)
        result = cast_ray(context, origin, direction)

        if result is not None:
            obj, hit, normal, face = result
            if use_normals:
                new_direction = obj.matrix_world @ normal.copy()
                new_direction.negate()
                new_direction.normalize()
            else:
                new_direction = direction

            back_hit, back_normal, back_face = cast_ray_at(obj, hit + new_direction * 0.01, new_direction)
            if back_hit is not None:
                back_hit_world = obj.matrix_world @ back_hit
                center_pos = hit + ((back_hit_world - hit) / 2)

                active_obj = bpy.context.active_object
                if active_obj is not None and active_obj.mode == 'EDIT':
                    armature = active_obj.data  # type: Armature
                    local_center_pos = obj.matrix_world.copy().inverted() @ center_pos
                    edit_bones = armature.edit_bones

                    if self.last_bone is not None:
                        self.last_bone.head = local_center_pos

                    if not complete_chain:
                        new_bone = edit_bones.new('new')
                        new_bone.tail = local_center_pos
                        new_bone.head = local_center_pos * 1.1

                        if self.last_bone is not None:
                            new_bone.parent = self.last_bone

                        self.last_bone = new_bone

    def modal(self, context, event):
        context.area.tag_redraw()

        if event.type == 'MOUSEMOVE':
            self.mouse_pos = (event.mouse_region_x, event.mouse_region_y)
        elif event.type in {'MIDDLEMOUSE', 'WHEELUPMOUSE', 'WHEELDOWNMOUSE'}:
            return {'PASS_THROUGH'}
        elif event.type == 'LEFTMOUSE':
            self.main(context, event, complete_chain=event.ctrl, use_normals=event.shift)
            if event.ctrl:
                return {'FINISHED'}
            else:
                return {'RUNNING_MODAL'}
        elif event.type in {'RIGHTMOUSE', 'ESC'}:
            bpy.types.SpaceView3D.draw_handler_remove(self._handle, 'WINDOW')
            return {'CANCELLED'}
        else:
            return {'PASS_THROUGH'}

        return {'RUNNING_MODAL'}

    def invoke(self, context, event):
        if context.space_data.type == 'VIEW_3D':
            self._handle = bpy.types.SpaceView3D.draw_handler_add(ui, (self, context), 'WINDOW', 'POST_PIXEL')
            context.window_manager.modal_handler_add(self)
            return {'RUNNING_MODAL'}
        else:
            self.report({'WARNING'}, "Active space must be a View3d")
            return {'CANCELLED'}
