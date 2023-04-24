import bpy
import os
from bpy.props import StringProperty

bl_info = {
    "Ofek David": "Project Organized",
    "description": "Start Organized with couple of clicks, work smarter work faster",
    "author": "Ofek, ChatGPT",
    "version": (1, 0),
    "blender": (3, 5, 0),
    "location": "View3D > UI > Project",
    "warning": "", # used for warning icon and text in addons panel
    "doc_url": "https://github.com/ofekdavid/Project_Organize_Blender",
    "support": "COMMUNITY",
    "category": "Import-Export",
}

class SelectFolderOperator(bpy.types.Operator):
    bl_idname = "object.select_folder"
    bl_label = "Select Folder"
    bl_description = "Select the folder where you want to create your project"
    
    directory: StringProperty(subtype='DIR_PATH')
    
    def execute(self, context):
        context.scene.folder_path = self.directory
        return {'FINISHED'}
    
    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

class CreateFoldersOperator(bpy.types.Operator):
    bl_idname = "object.create_folders"
    bl_label = "Create Project"
    bl_description = "Create the necessary subdirectories within the selected folder"

    subdirs = {
        'Scenes': {
            'WIP': ''
        },
        'Sourceimages': {
            'References': '',
            'Materials': '',
            'Substance': ''
            
        },
        'Assets': '',
        'Images': {
            'Render Sequence': ''
        },
        'Movies': '',
        'Sounds': '',
        'Scripts': '',
        'Preferences': ''
    }

    def create_subdirectories(self, folder_path):
        # Create subdirectories within the selected directory
        for subdir in self.subdirs:
            subdir_path = os.path.join(folder_path, subdir)
            if isinstance(self.subdirs[subdir], dict):
                for subsubdir in self.subdirs[subdir]:
                    subsubdir_path = os.path.join(subdir_path, subsubdir)
                    os.makedirs(subsubdir_path)
            else:
                os.makedirs(subdir_path)

    def execute(self, context):
        # Create folders here
        folder_path = context.scene.folder_path
        self.create_subdirectories(folder_path)
        return {'FINISHED'}
    
class CreateProjectPanel(bpy.types.Panel):
    bl_label = "Create Project"
    bl_idname = "OBJECT_PT_create_project"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Project'

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        
        row = layout.row()
        row.prop(scene, "folder_path", text="Folder Path")
        
        row = layout.row()
        row.operator("object.select_folder")
        
        row = layout.row()
        row.operator("object.create_folders")
        
        row = layout.row()
        row.operator("object.set_project")

class SetProjectOperator(bpy.types.Operator):
    bl_idname = "object.set_project"
    bl_label = "Set Project"
    bl_description = "Create a new project with the necessary subdirectories"
    
    def execute(self, context):
        folder_path = context.scene.folder_path
        
        # Set the Blender preferences file paths to the project folders
        context.preferences.filepaths.render_output_directory = os.path.join(folder_path, "Images" , "Render Sequence/")
        context.preferences.filepaths.texture_directory = os.path.join(folder_path, "Sourceimages" , "Materials/")
        context.preferences.filepaths.sound_directory = os.path.join(folder_path, "Sounds")
        context.preferences.filepaths.script_directory = os.path.join(folder_path, "Scripts")
        return {'FINISHED'}
    
def register():
    bpy.types.Scene.folder_path = bpy.props.StringProperty(name="Folder Path")
    bpy.utils.register_class(SelectFolderOperator)
    bpy.utils.register_class(CreateFoldersOperator)
    bpy.utils.register_class(CreateProjectPanel)
    bpy.utils.register_class(SetProjectOperator) # register the new operator

def unregister():
    bpy.utils.unregister_class(SelectFolderOperator)
    bpy.utils.unregister_class(CreateFoldersOperator)
    bpy.utils.unregister_class(CreateProjectPanel)
    bpy.utils.unregister_class(SetProjectOperator) # unregister the new operator
    del bpy.types.Scene.folder_path

if __name__ == "__main__":
    register()
