from flttoolkit.types import FLT_OBJECT

inst = FLT_OBJECT(0xFFFFA50F35610260)

print(inst.is_instance_type)
print(inst.is_volume_type)
print(inst.PointerCount)

print(inst.for_each(lambda obj: print(hex(obj.Flags))))
