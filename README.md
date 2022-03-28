# zanim tools

Some (eventually) helpful Python scripts for sculpting, rigging, and animating in Blender.

## Tools

### Armature

Tools for building and editing armatures.

#### Create armature from mouse points

Place bones inside a mesh by casting rays from the viewport.

##### Function

Speeds up the workflow of using the 3D cursor to select midpoints between opposing vertices using a ray cast from the
viewport camera to find a selected vertex, and a second ray cast to find the opposing vertex in the direction of the ray.
The direction of the second ray is derived from the screen space ray direction by default. It can cast rays in the direction of the inverse normal at the first selected vertex to attempt to get the vertex "behind" from any angle.

Bones will automatically be created at the midpoint of the two vertices, and any successive bones auto-parented.

##### Usage

Controls:

- <kbd>Left Click</kbd> - Place a new bone at the clicked position inside the mesh.
- <kbd>Shift</kbd> + <kbd>Left Click</kbd> - Place a new bone at the clicked position inside the mesh, using vertex
  normals of the first intersection to generate the second ray.
- <kbd>Ctrl</kbd> + <kbd>Left Click</kbd> - Update the tail of the last placed bone and complete the current chain.R

https://user-images.githubusercontent.com/1180094/160496573-c1df80b7-75e4-4473-b5b7-c9eb275edde6.mp4