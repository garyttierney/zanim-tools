import bpy
from mathutils import Vector


def cast_ray_at(obj: bpy.types.Object, origin: Vector, direction: Vector):
    matrix_inv = obj.matrix_world.copy().inverted()
    ray_origin_obj = matrix_inv @ origin

    success, location, normal, face_index = obj.ray_cast(ray_origin_obj, direction)

    if success:
        return location, normal, face_index
    else:
        return None, None, None


def cast_ray(ctx: bpy.types.Context, origin: Vector, direction: Vector):
    def visible_objects_and_duplis():
        depsgraph = ctx.evaluated_depsgraph_get()
        for dup in depsgraph.object_instances:
            if dup.is_instance:  # Real dupli instance
                obj = dup.instance_object
                yield obj, dup.matrix_world.copy()
            else:  # Usual object
                obj = dup.object
                yield obj, obj.matrix_world.copy()

    best_length_squared = -1.0
    best_result = None

    for obj, matrix in visible_objects_and_duplis():
        if obj.type == 'MESH':
            hit, normal, face_index = cast_ray_at(obj, origin, direction)
            if hit is not None:
                hit_world = matrix @ hit
                length_squared = (hit_world - origin).length_squared
                if best_result is None or length_squared < best_length_squared:
                    best_length_squared = length_squared
                    best_result = (obj, hit, normal, face_index)

    if best_result is not None:
        return best_result
