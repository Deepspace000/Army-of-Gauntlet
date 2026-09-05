"""A chibi warrior in the proportions of the game's champions: big round head,
short thick body, stubby limbs, horned helm, cape and axe. Built from
primitives, flat-shaded materials, rendered from the front, three-quarter and
side with Eevee. Output: warrior_front.png, warrior_quarter.png, warrior_side.png."""
import bpy, math, os, sys

OUT = r"C:\Users\mirko\Downloads\V-CODE GAMES\blender"
os.makedirs(OUT, exist_ok=True)

bpy.ops.wm.read_factory_settings(use_empty=True)
scene = bpy.context.scene

def mat(name, rgb, rough=0.6, metal=0.0, emit=None):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    bsdf = m.node_tree.nodes["Principled BSDF"]
    bsdf.inputs["Base Color"].default_value = (*rgb, 1)
    bsdf.inputs["Roughness"].default_value = rough
    bsdf.inputs["Metallic"].default_value = metal
    if emit:
        bsdf.inputs["Emission Color"].default_value = (*emit, 1)
        bsdf.inputs["Emission Strength"].default_value = 4.0
    return m

def hexc(h):
    h = h.lstrip('#'); return tuple(int(h[i:i+2], 16)/255 for i in (0, 2, 4))

M_SKIN  = mat("skin",  hexc("#e8b07a"))
M_HAIR  = mat("hair",  hexc("#3a2010"))
M_TUNIC = mat("tunic", hexc("#8c0a14"))
M_TROUS = mat("trousers", hexc("#3a0608"))
M_BOOT  = mat("boot",  hexc("#1a0404"))
M_STEEL = mat("steel", hexc("#c8c8d8"), rough=0.35, metal=0.8)
M_HORN  = mat("horn",  hexc("#e8e4d0"), rough=0.5)
M_CAPE  = mat("cape",  hexc("#4a0008"))
M_EYE   = mat("eye",   hexc("#ff2a2a"), emit=hexc("#ff2a2a"))
M_WOOD  = mat("wood",  hexc("#5a3a1a"))
M_GROUND= mat("ground",hexc("#2a2436"), rough=0.9)

parts = []
def add(op, m, loc, scale=(1,1,1), rot=(0,0,0), **kw):
    op(location=loc, rotation=rot, **kw)
    o = bpy.context.active_object
    o.scale = scale
    o.data.materials.append(m)
    bpy.ops.object.shade_smooth() if m not in (M_STEEL, M_WOOD) else None
    parts.append(o)
    return o

S = bpy.ops.mesh.primitive_uv_sphere_add
C = bpy.ops.mesh.primitive_cylinder_add
B = bpy.ops.mesh.primitive_cube_add
K = bpy.ops.mesh.primitive_cone_add

# ---- proportions: head about a third of the height, as in the sprites
# body
add(B, M_TUNIC, (0, 0, 1.05), scale=(0.55, 0.38, 0.45))               # torso
add(B, M_TROUS, (0, 0, 0.55), scale=(0.5, 0.34, 0.22))                # hips
add(B, M_STEEL, (0, 0, 1.08), scale=(0.58, 0.41, 0.16))               # chest plate band
for sx in (-1, 1):
    add(C, M_TROUS, (sx*0.24, 0, 0.32), scale=(0.16, 0.16, 0.22))     # legs
    add(B, M_BOOT, (sx*0.24, 0.05, 0.08), scale=(0.2, 0.28, 0.1))     # boots
    add(C, M_SKIN, (sx*0.72, 0, 1.0), scale=(0.15, 0.15, 0.3), rot=(0, 0, 0))   # arms
    add(S, M_STEEL, (sx*0.72, 0, 1.35), scale=(0.26, 0.26, 0.2))     # pauldrons
    add(S, M_SKIN, (sx*0.72, 0, 0.66), scale=(0.17, 0.17, 0.17))     # fists
# head: the big round head of the arcade chibi
head = add(S, M_SKIN, (0, 0, 2.05), scale=(0.62, 0.6, 0.6))
add(S, M_HAIR, (0, -0.12, 2.2), scale=(0.6, 0.62, 0.45))              # hair mass, behind the brow
add(S, M_STEEL, (0, 0, 2.35), scale=(0.66, 0.64, 0.42))               # helm dome
add(B, M_STEEL, (0, 0.5, 2.05), scale=(0.68, 0.06, 0.22))             # helm brow band
for sx in (-1, 1):
    add(K, M_HORN, (sx*0.7, 0.1, 2.55), scale=(0.2, 0.2, 0.7), rot=(-0.4, sx*1.1, 0), radius1=0.2, depth=1.0)   # horns, wide and forward
    add(S, M_EYE, (sx*0.22, 0.56, 2.02), scale=(0.11, 0.06, 0.12))      # eyes, lit red
add(B, M_HAIR, (0, 0.6, 1.72), scale=(0.28, 0.06, 0.16))              # beard
# cape, hanging behind
add(B, M_CAPE, (0, -0.42, 1.05), scale=(0.62, 0.05, 0.85))
# axe in the right hand
add(C, M_WOOD, (0.98, 0.1, 1.0), scale=(0.05, 0.05, 0.9), rot=(0, 0.12, 0))
add(B, M_STEEL, (0.98, 0.1, 1.75), scale=(0.34, 0.06, 0.3))
add(B, M_STEEL, (1.22, 0.1, 1.75), scale=(0.12, 0.05, 0.42))         # the blade's flare

bpy.ops.object.select_all(action='DESELECT')
for o in parts: o.select_set(True)
bpy.context.view_layer.objects.active = parts[0]
bpy.ops.object.join()
warrior = bpy.context.active_object
warrior.name = "BloodWarrior"

# ground disc and a hard cast shadow, like the sprites' drop shadow
bpy.ops.mesh.primitive_plane_add(size=8, location=(0, 0, 0))
ground = bpy.context.active_object; ground.data.materials.append(M_GROUND)

# lights: key from the upper left as in the game, a cool rim from behind
def light(name, kind, loc, energy, color=(1, 1, 1), size=2.0):
    l = bpy.data.lights.new(name, kind); l.energy = energy; l.color = color
    if kind == 'AREA': l.size = size
    o = bpy.data.objects.new(name, l); scene.collection.objects.link(o)
    o.location = loc
    o.rotation_euler = (math.atan2(math.hypot(loc[0], loc[1]), loc[2]), 0, math.atan2(loc[1], loc[0]) + math.pi/2) if kind != 'POINT' else (0,0,0)
    return o
key = light("key", 'AREA', (-3, 3, 5), 900, (1.0, 0.95, 0.85), 3)
key.rotation_euler = (math.radians(50), 0, math.radians(-140))
rim = light("rim", 'AREA', (2.5, -3, 3.5), 500, (0.6, 0.75, 1.0), 2)
rim.rotation_euler = (math.radians(60), 0, math.radians(40))
fill = light("fill", 'POINT', (3, 4, 2), 200, (1, 0.9, 0.9))

# camera
cam_data = bpy.data.cameras.new("cam"); cam_data.lens = 50
cam = bpy.data.objects.new("cam", cam_data); scene.collection.objects.link(cam)
scene.camera = cam

scene.render.engine = 'BLENDER_EEVEE'
scene.render.resolution_x = 640; scene.render.resolution_y = 800
scene.render.film_transparent = False
scene.world = bpy.data.worlds.new("w"); scene.world.use_nodes = True
scene.world.node_tree.nodes["Background"].inputs[0].default_value = (0.08, 0.06, 0.12, 1)
scene.world.node_tree.nodes["Background"].inputs[1].default_value = 1.0

def shoot(name, az_deg):
    a = math.radians(az_deg)
    d = 7.0
    cam.location = (d*math.sin(a), d*math.cos(a), 2.6)      # the face is on +Y
    # aim at the chest
    import mathutils
    direction = mathutils.Vector((0, 0, 1.3)) - cam.location
    cam.rotation_euler = direction.to_track_quat('-Z', 'Y').to_euler()
    scene.render.filepath = os.path.join(OUT, f"warrior_{name}.png")
    bpy.ops.render.render(write_still=True)
    print("rendered", scene.render.filepath)

shoot("front", 0)
shoot("quarter", 40)
shoot("side", 90)
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(OUT, "warrior.blend"))
print("DONE")
