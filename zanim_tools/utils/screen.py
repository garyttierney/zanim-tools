import bpy
from bpy_extras import view3d_utils
from mathutils import Vector


def screen_to_world_ray(ctx: bpy.types.Context, x: int, y: int) -> Vector:
    region = ctx.region
    rv3d = ctx.region_data
    coord = x, y

    view_vector = view3d_utils.region_2d_to_vector_3d(region, rv3d, coord)
    view_origin = view3d_utils.region_2d_to_origin_3d(region, rv3d, coord)

    return (view_origin, view_vector)
