import pkg_resources

from cffi import FFI


ffi = FFI()
ffi.cdef("""
    double haversine(double, double, double, double);
""")

DYLIB_PATH = pkg_resources.resource_filename(
    'denis',
    'libdenis.macos.dylib'
)

lib = ffi.dlopen(DYLIB_PATH)

def haversine(lat_lng1, lat_lng2):
    return lib.haversine(
        lat_lng1[0],
        lat_lng1[1],
        lat_lng2[0],
        lat_lng2[1],
    )
