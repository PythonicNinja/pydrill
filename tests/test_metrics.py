from pydrill.client import PyDrill
drill = PyDrill(host='localhost', port=8047)

if not drill.is_active():
    raise ImproperlyConfigured('Please run Drill first')

metrics = drill.metrics()
for data in drill.metrics():
    print( data )

print(metrics.keys)
print(metrics.data)
print(metrics.values)
print(drill.metrics().max_direct_memory)
