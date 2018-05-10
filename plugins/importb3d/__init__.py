# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

# <pep8 compliant>

bl_info = {
    'name': 'B3D importer',
    'author': 'Yuriy Gladishenko, Andrey Prozhoga',
    'version': (0, 1, 13),
    'blender': (2, 7, 9),
    'api': 34893,
    'description': 'This script imports the King of the Road b3d',
    'warning': '',
    'wiki_url': 'http://wiki.blender.org/index.php/Extensions:2.5/Py/Scripts/'\
        'Import-Export/M3_Import',
    'tracker_url': 'http://projects.blender.org/tracker/index.php?'\
       'func=detail&aid=24017',
    'category': 'Import-Export'}


# To support reload properly, try to access a package var, if it's there,
# reload everything
if "bpy" in locals():
    import imp
    if 'importb3d' in locals():
        imp.reload(importb3d)
#   if 'export_m3' in locals():
#       imp.reload(exportb3d)

import time
import datetime
import bpy
from bpy.props import StringProperty, BoolProperty
from bpy_extras.io_utils import ImportHelper, ExportHelper


class ImportB3D(bpy.types.Operator, ImportHelper):
    '''Import from B3D file format (.b3d)'''
    bl_idname = 'import_scene.kotr_b3d'
    bl_label = 'Import B3D'

    filename_ext = '.b3d'
    filter_glob = StringProperty(default='*.b3d', options={'HIDDEN'})

    use_image_search = BoolProperty(name='Image Search',
                        description='Search subdirectories for any associated'\
                                    'images', default=True)

    def execute(self, context):
        from . import importb3d
        print('Importing file', self.filepath)
        t = time.mktime(datetime.datetime.now().timetuple())
        with open(self.filepath, 'rb') as file:
            importb3d.read(file, context, self, self.filepath)
        t = time.mktime(datetime.datetime.now().timetuple()) - t
        print('Finished importing in', t, 'seconds')
        return {'FINISHED'}

		
class ExportB3D(bpy.types.Operator, ImportHelper):
    '''Export to B3D file format (.b3d)'''
    bl_idname = 'export_scene.kotr_b3d'
    bl_label = 'Export B3D'

    filename_ext = '.b3d'
    filter_glob = StringProperty(default='*.b3d', options={'HIDDEN'})

    use_image_search = BoolProperty(name='Image Search',
                        description='Search subdirectories for any associated'\
                                    'images', default=True)

    def execute(self, context):
        from . import exportb3d
        print('Exporting file', self.filepath)
        t = time.mktime(datetime.datetime.now().timetuple())
        with open(self.filepath+'.b3d','wb') as file:
            exportb3d.write(file, context, self, self.filepath)
        t = time.mktime(datetime.datetime.now().timetuple()) - t
        print('Finished exporting in', t, 'seconds')
        return {'FINISHED'}

		
def menu_func_import(self, context):
    self.layout.operator(ImportB3D.bl_idname, text='KOTR B3D (.b3d)')


def menu_func_export(self, context):
   self.layout.operator(ExportB3D.bl_idname, text='KOTR B3D (.b3d)')


def register():
    bpy.utils.register_module(__name__)
    bpy.types.INFO_MT_file_import.append(menu_func_import)
    bpy.types.INFO_MT_file_export.append(menu_func_export)


def unregister():
    bpy.utils.unregister_module(__name__)
    bpy.types.INFO_MT_file_import.remove(menu_func_import)
    bpy.types.INFO_MT_file_export.remove(menu_func_export)


if __name__ == "__main__":
    register()
