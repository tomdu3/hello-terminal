t_obj = t"hello {1}"
print("dir(t_obj.interpolations[0]):", dir(t_obj.interpolations[0]))
print("t_obj.interpolations[0].value:", repr(getattr(t_obj.interpolations[0], 'value', None)))
print("t_obj.interpolations[0].expr:", getattr(t_obj.interpolations[0], 'expr', None))

v = t_obj.interpolations[0]
print("v[0] (value):", repr(v[0]) if hasattr(v, '__getitem__') else "not subscriptable")
print("v.getvalue():", repr(v.getvalue()) if hasattr(v, 'getvalue') else "no getvalue")
