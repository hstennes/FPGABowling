import numpy as np
from PIL import Image

# Vector operations
def normalize(v):
    return v / np.linalg.norm(v)

def magnitude(v):
    return np.linalg.norm(v)

def dot(v1, v2):
    return np.dot(v1, v2)

# Ray-sphere intersection
def intersect_sphere(origin, direction, sphere):
    oc = origin - sphere['center']

    # print(oc)

    a = dot(direction, direction)  #30
    b = 2.0 * dot(oc, direction)   #39
    # print(oc, direction, dot(oc, direction))
    c = dot(oc, oc) - sphere['radius'] ** 2 #48

    # print(a, b, c)

    discriminant = b ** 2 - 4 * a * c
    if discriminant < 0:
        return None  # No intersection
    t1 = (-b - np.sqrt(discriminant)) / (2.0 * a)
    t2 = (-b + np.sqrt(discriminant)) / (2.0 * a)
    return min(t1, t2)

# Ray-cylinder intersection
def intersect_cylinder(origin, direction, cylinder):

    # print(origin, direction, cylinder["center"], cylinder["direction"])

    # Cylinder's direction should be normalized
    ca = cylinder['direction']
    oc = origin - cylinder['center']
    
    # Calculate the coefficients for the quadratic equation
    a = (dot(direction, direction) - dot(direction, ca) ** 2) / 4
    b = dot(direction, oc) - dot(direction, ca) * dot(oc, ca)
    c = dot(oc, oc) - dot(oc, ca) ** 2 - cylinder['radius'] ** 2
    discriminant = b ** 2 - 4 * a * c
    
    if discriminant < 0:
        return None  # No intersection

    # Solving the quadratic equation
    sqrt_discriminant = np.sqrt(discriminant)
    t1 = (-b - sqrt_discriminant) / (2 * a)
    t2 = (-b + sqrt_discriminant) / (2 * a)

    # Find the closest valid intersection
    # t = min(t1, t2) if t1 > 0 else (t2 if t2 > 0 else None)
    t = min(t1 / 2, t2 / 2)

    if t is None:
        return None

    # Check if the intersection point is within the height of the cylinder
    hit_point = origin + direction * t
    height = dot(hit_point - cylinder['center'], ca)
    if 0 <= height <= cylinder['height']:
        return t
    return None

# Main render function with support for spheres and cylinders
def render(camera, spheres, cylinders, lights, width=400, height=300, fov=90):
    aspect_ratio = width / height
    angle = np.tan(np.radians(fov / 2))
    img = Image.new("RGB", (width, height))
    pixels = img.load()

    PX_MUL = 2 / width * angle * aspect_ratio
    PX_ADD = -angle * aspect_ratio
    PY_MUL = -2 / height * angle
    PY_ADD = angle

    print([y * PY_MUL + PY_ADD for y in (240, 224, 100)])

    print(PX_MUL, PX_ADD, PY_MUL, PY_ADD)

    for y in range(height):
        for x in range(width):
            # Normalized screen space coordinates
            # px = (2 * (x) / width - 1) * angle * aspect_ratio
            # py = (1 - 2 * (y) / height) * angle

            px = x * PX_MUL + PX_ADD
            py = y * PY_MUL + PY_ADD
            direction = np.array([px, py, -1]) # Camera pointing along -z

            # Find nearest intersection
            color = np.array([0, 0, 0])
            min_dist = float('inf')

            # Check intersections with spheres
            for sphere in spheres:
                dist = intersect_sphere(camera, direction, sphere)
                if dist is not None and dist < min_dist:


                    min_dist = dist
                    # Compute point of intersection
                    hit_point = camera + direction * dist
                    normal = hit_point - sphere['center']
                    # Accumulate light contribution from each source
                    sphere_color = np.array(sphere['color'])
                    final_color = np.zeros(3)
                    for light in lights:
                        light_dir = light['position'] - hit_point
                        intensity = dot(normal, light_dir) / 16
                        final_color += intensity * sphere_color

                    color = np.clip(final_color, 0, 255).astype(int)

                    # print("guys we found the sphere")
                    # print(hit_point, normal, color)
                    # exit()

            # Check intersections with cylinders
            c_count = 0
            for cylinder in cylinders:
                dist = intersect_cylinder(camera, direction, cylinder)
                if dist != None: c_count += 1
                if dist is not None and dist < min_dist:

                    # print("guys we found the cylinder", dist)
                    # exit() 29

                    min_dist = dist
                    # Compute point of intersection
                    hit_point = camera + direction * dist
                    hit_height = hit_point[1] - cylinder["center"][1]
                    ca = cylinder['direction']
                    pre_normal = hit_point - cylinder['center']
                    normal = pre_normal - dot(pre_normal, ca) * ca

                    # Accumulate light contribution from each source
                    cylinder_color = np.array(cylinder['color'])
                    if 2 < hit_height < 2.2: cylinder_color = np.array([255, 0, 0])
                    final_color = np.zeros(3)
                    for light in lights:
                        light_dir = light['position'] - hit_point
                        intensity = dot(normal, light_dir) / 16

                        final_color += intensity * cylinder_color

                    color = np.clip(final_color, 0, 255).astype(int)
                    
                    pass

            # Set the pixel color
            if x == 320 and (y == 223 or y == 224):
                print(camera, direction, c_count)
                pixels[x, y] = (255, 0, 255)
            else:
                pixels[x, y] = tuple(color)

    return img

# Define camera, spheres, cylinders, and multiple light sources
camera = np.array([0, 0, 5])
spheres = [
    {'center': np.array([0, -5, -5]), 'radius': 1, 'color': [0, 255, 0]},  # Green sphere
]
cylinders = [
    {'center': np.array([0, -5, -22]), 'direction': normalize(np.array([0, 1, 0])), 'radius': 0.7, 'height': 3, 'color': [255, 255, 255]},
    {'center': np.array([0, -5, -20]), 'direction': normalize(np.array([0, 1, 0])), 'radius': 0.7, 'height': 3, 'color': [255, 255, 255]},
    {'center': np.array([0, -5, -18]), 'direction': normalize(np.array([0, 1, 0])), 'radius': 0.7, 'height': 3, 'color': [255, 255, 255]},
    {'center': np.array([0, -5, -16]), 'direction': normalize(np.array([0, 1, 0])), 'radius': 0.7, 'height': 3, 'color': [255, 255, 255]},
    {'center': np.array([0, -5, -14]), 'direction': normalize(np.array([0, 1, 0])), 'radius': 0.7, 'height': 3, 'color': [255, 255, 255]},
    {'center': np.array([0, -5, -12]), 'direction': normalize(np.array([0, 1, 0])), 'radius': 0.7, 'height': 3, 'color': [255, 255, 255]},
    {'center': np.array([0, -5, -10]), 'direction': normalize(np.array([0, 1, 0])), 'radius': 0.7, 'height': 3, 'color': [255, 255, 255]},
    {'center': np.array([0, -5, -8]), 'direction': normalize(np.array([0, 1, 0])), 'radius': 0.7, 'height': 3, 'color': [255, 255, 255]},
    {'center': np.array([0, -5, -6]), 'direction': normalize(np.array([0, 1, 0])), 'radius': 0.7, 'height': 3, 'color': [255, 255, 255]},
    {'center': np.array([0, -5, -4]), 'direction': normalize(np.array([0, 1, 0])), 'radius': 0.7, 'height': 3, 'color': [255, 255, 255]},
]
lights = [
    {'position': np.array([0, 5, 8]), 'intensity': 0.7},
    # {'position': np.array([0, 10, -5]), 'intensity': 0.5},
]

# Render and save the image
image = render(camera, spheres, cylinders, lights, width=640, height=360)
image.show()
