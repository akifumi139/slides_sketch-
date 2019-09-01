bl_info = {
    "name" : "slides_sketch ",
    "author" : "akifumi",
    "description" : "Slide sketch",
    "blender" : (2, 80, 0),
    "version" : (0, 0, 2),
    "location" : "View3D > N panel > slide",
    "warning" : "",
    "category" : "Generic"
}

import bpy
import glob
import os
import math
from bpy.props import (StringProperty,
                       BoolProperty,
                       IntProperty,
                       FloatProperty,
                       FloatVectorProperty,
                       EnumProperty,
                       PointerProperty,
                       )
from bpy.types import (Panel,
                       Menu,
                       Operator,
                       PropertyGroup,
                       )
page_num=1
filepath=""
image_cnt=1

class InitProperties(PropertyGroup):

    path_image: StringProperty(
        name = "",
        description="Choose a directory:",
        default="",
        maxlen=1024,
        subtype='DIR_PATH'
        )

class Reload_OT_Operator(bpy.types.Operator):
    bl_idname ="view3d.reload_btn"
    bl_label ="Reload:image_cnt"
    bl_description ="Reload:"

    def execute(self, context):
        scene = context.scene
        mytool = scene.Init_Prop
        global filepath,image_cnt,page_num
        filepath = mytool.path_image
        image_cnt=len(glob.glob(filepath+'/*[.jpeg, .png,.jpg]'))

        bpy.ops.object.armature_basic_human_metarig_add()
        obj=bpy.context.object
        obj.name='rig'

        self.report({'INFO'}, filepath)
        return{'FINISHED'}

class Slide_OT_Move(bpy.types.Operator):
    bl_idname = "slide.move"
    bl_label = "NEXT"
    bl_options = {'REGISTER', 'UNDO'}

    Move : bpy.props.IntProperty()
    def execute(self, context):
        global page_num
        page_num=page_num+self.Move
        if(page_num%(image_cnt+1)==0):
            page_num=(page_num-image_cnt)*self.Move
        

        self.report({'INFO'}, str(page_num))
        chang_object(self)
    
        return {'FINISHED'}

class SaveBone_OT_Operator(bpy.types.Operator):
    bl_idname ="view3d.save_bone"
    bl_label ="Save bone_laction"
    bl_description ="Record bones condition"

    def execute(self, context):

        return{'FINISHED'}



class SlideImage_PT_Panel(bpy.types.Panel):
    bl_idname ="SlideImage_PT_Panel"
    bl_label ="Slide Image Panel"
    bl_category ="Slide"
    bl_space_type ="VIEW_3D"
    bl_region_type ="UI"


    def draw (self,context):
        layout =self.layout

        scene = context.scene
        mytool = scene.Init_Prop

        path = layout.column(align=True).row()

        path.prop(mytool, "path_image")
        path.alignment = 'LEFT'
        path.operator('view3d.reload_btn',text="Reload")

        btn = layout.column(align=True).row()
        btn.alignment = 'CENTER'

        btn.operator('slide.move',text="BACK").Move =-1
        btn.label(text='    '+str(page_num))
        btn.operator('slide.move',text="NEXT").Move =1

        
        layout.operator('view3d.save_bone',text="Save_bone")


classes =(
    InitProperties,
    Reload_OT_Operator,
    Slide_OT_Move,
    SaveBone_OT_Operator,
    SlideImage_PT_Panel
    )

register_tmp, unregister =bpy.utils.register_classes_factory(classes)

def register():
    register_tmp()

    bpy.types.Scene.Init_Prop = PointerProperty(type=InitProperties)

def chang_object(self):
    global filepath
    remove_list=['front_image']
    for item in bpy.data.objects:
        if item.name in remove_list:
            bpy.data.objects.remove(item)


    bpy.ops.object.load_background_image(filepath = filepath+"img"+str(page_num)+".png")

    obj=bpy.context.object
    obj.name='front_image'
    obj.location=[0,0,0]
    obj.rotation_euler=[math.radians(90),0,0]


    self.report({'INFO'}, filepath+"img"+str(page_num)+".png")
