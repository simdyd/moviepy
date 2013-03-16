from deviceatlas.api import DaApi
from distutils.sysconfig import get_python_lib
da = DaApi()
path_to_device_atlas_json = "%s/deviceatlas/DeviceAtlas.json" % get_python_lib()
tree = da.getTreeFromFile(path_to_device_atlas_json)
da.getTreeRevision(tree)
ua = 'Mozilla/5.0 (iPhone; U; CPU like Mac OS X; en) AppleWebKit/420+ (KHTML, like Gecko) Version/3.0 Mobile/1A543 Safari/419.3'
da.getProperties(tree, ua)