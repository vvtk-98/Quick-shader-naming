def create_and_assign_lambert_shader_single(obj):
    short_name = cmds.ls(obj, shortNames=True)[0]
    base_name = short_name.split("geo")[0].rstrip("_")
    shader_name = f"{base_name}_SHD"
    shading_group_name = f"{base_name}_SG"

    shader = cmds.shadingNode('lambert', asShader=True, name=shader_name)
    shading_group = cmds.sets(renderable=True, noSurfaceShader=True, empty=True, name=shading_group_name)
    cmds.connectAttr(shader + '.outColor', shading_group + '.surfaceShader', force=True)

    faces = cmds.ls(obj + '.f[*]', flatten=True)
    cmds.sets(faces, edit=True, forceElement=shading_group)

    print(f"Assigned {shader_name} to all faces of {obj}")

def create_and_assign_lambert_shader_multiple(objects):
    result = cmds.promptDialog(
        title='Shader Name',
        message='Enter Name for Shader and Shader Group:',
        button=['OK', 'Cancel'],
        defaultButton='OK',
        cancelButton='Cancel',
        dismissString='Cancel'
    )

    if result == 'OK':
        base_name = cmds.promptDialog(query=True, text=True)
        shader_name = f"{base_name}_SHD"
        shading_group_name = f"{base_name}_SG"

        shader = cmds.shadingNode('lambert', asShader=True, name=shader_name)
        shading_group = cmds.sets(renderable=True, noSurfaceShader=True, empty=True, name=shading_group_name)
        cmds.connectAttr(shader + '.outColor', shading_group + '.surfaceShader', force=True)

        for obj in objects:
            faces = cmds.ls(obj + '.f[*]', flatten=True)
            cmds.sets(faces, edit=True, forceElement=shading_group)

        print(f"Assigned {shader_name} to all faces of {len(objects)} objects")
    else:
        print("Operation cancelled by user.")


def create_and_assign_lambert_shader_selected_faces():
    selected_faces = cmds.ls(selection=True, flatten=True)

    if not selected_faces:
        cmds.warning("Please select at least one face before running this function.")
        return

    result = cmds.promptDialog(
        title='Shader Name',
        message='Enter name for the Shader:',
        button=['OK', 'Cancel'],
        defaultButton='OK',
        cancelButton='Cancel',
        dismissString='Cancel'
    )

    if result == 'OK':
        base_name = cmds.promptDialog(query=True, text=True)
        shader_name = f"{base_name}_SHD"
        shading_group_name = f"{base_name}_SG"

        shader = cmds.shadingNode('lambert', asShader=True, name=shader_name)
        shading_group = cmds.sets(renderable=True, noSurfaceShader=True, empty=True, name=shading_group_name)
        cmds.connectAttr(shader + '.outColor', shading_group + '.surfaceShader', force=True)

        cmds.sets(selected_faces, edit=True, forceElement=shading_group)

        print(f"Assigned {shader_name} to {len(selected_faces)} selected faces")
    else:
        print("Operation cancelled by user.")


selection = cmds.ls(selection=True, long=True)

if not selection:
    cmds.warning("Please select at least one object or face before running this script.")
elif cmds.filterExpand(selection, selectionMask=34):
    create_and_assign_lambert_shader_selected_faces()
elif len(selection) == 1:
    create_and_assign_lambert_shader_single(selection[0])
else:
    create_and_assign_lambert_shader_multiple(selection)