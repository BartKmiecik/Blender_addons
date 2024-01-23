import json

with open('D:\BlenderAddons\Blender_addons\MultipleFileTest\M_DLL\Selections.json', 'r') as d:
        customData = d.read()
        t1 = customData
        t2 = json.dumps(t1)
        t3 = json.loads(t1)

print(t1)
print(t2)
print(t3)