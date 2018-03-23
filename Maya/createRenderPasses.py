#Custom Render Elements Maya Version 4.0.0
#Bryanna London
#!/usr/bin/env python
 
#2.0 adds a wireframe element
#3.0 changed the way UV pass was made so it works for UDIM uvs.
#4.0 change noise pass to RGB noise
#5.0 adds curvature element 
 
import maya.cmds as cmds
import maya.mel as mel
 
#Create Ambient Occlusion Render Element
def createOcc():
 
    ao = mel.eval('vrayAddRenderElement ExtraTexElement')
    #rename Occlusion
    occlusion = cmds.rename(ao , 'Occlusion')
    #set Explicit channel name to Occlusion
    cmds.setAttr(occlusion + '.vray_explicit_name_extratex', 'Occlusion', type = 'string')
    #Turn off affect matte objects
    cmds.setAttr(occlusion + '.vray_affectmattes_extratex', 0)
 
    #create vray dirt and connect place2dTextureNodeimport time
    vrayDirt = cmds.shadingNode('VRayDirt', name = 'occ_dirt', asTexture = True)
    cmds.setAttr(vrayDirt + '.subdivs' , 32)
    place2dTextureNode = cmds.shadingNode('place2dTexture', asUtility = True)
    cmds.connectAttr(place2dTextureNode + '.outUV', vrayDirt + '.uvCoord')
    cmds.connectAttr(place2dTextureNode + '.outUvFilterSize', vrayDirt + '.uvFilterSize')
 
    #connect the vray dirt to occlusion element
    cmds.connectAttr(vrayDirt + '.outColor', occlusion + '.vray_texture_extratex')
 
#Create Fresnel Element
def createFresnel():
 
    fresnel = mel.eval('vrayAddRenderElement ExtraTexElement')
    #rename fresnel
    fresnelName = cmds.rename(fresnel , 'Fresnel')
    #set explicit channel name
    cmds.setAttr(fresnelName + '.vray_explicit_name_extratex', 'Fresnel', type = 'string')
    #Turn off affect matte objects
    cmds.setAttr(fresnelName + '.vray_affectmattes_extratex', 0)
 
    #create vray fresnel and connect place2dTextureNode
    vrayFresnel = cmds.shadingNode('VRayFresnel', asTexture = True)
    place2dTextureNodeF = cmds.shadingNode('place2dTexture', asUtility = True)
    cmds.connectAttr(place2dTextureNodeF + '.outUV', vrayFresnel + '.uvCoord')
    cmds.connectAttr(place2dTextureNodeF + '.outUvFilterSize', vrayFresnel + '.uvFilterSize')
 
    #connect the vray fresnel to fresnel element
    cmds.connectAttr(vrayFresnel + '.outColor', fresnelName + '.vray_texture_extratex')
 
#Create UV Element
def createUv():
 
    uv = mel.eval('vrayAddRenderElement ExtraTexElement')
    #rename UV
    uvPass = cmds.rename(uv , 'UV')
    #set explicit channel name
    cmds.setAttr(uvPass + '.vray_explicit_name_extratex', 'UV', type = 'string')
    #Turn off the three checkboxes
    cmds.setAttr(uvPass + '.vray_considerforaa_extratex', 1)
    cmds.setAttr(uvPass + '.vray_affectmattes_extratex', 0)
    cmds.setAttr(uvPass + '.vray_filtering_extratex', 1)
 
    #create Average Node
    plusNode = cmds.shadingNode('plusMinusAverage', asUtility = True)
 
    #Create U ramp
    uramp = cmds.shadingNode('ramp', asTexture = True)
    uRamp = cmds.rename(uramp, 'uRamp')
    cmds.setAttr(uRamp + '.type', 1)
    cmds.setAttr(uRamp + '.colorEntryList[0].color', 0,0,0, type = 'double3')
    cmds.setAttr(uRamp + '.colorEntryList[1].position', 1)
    cmds.setAttr(uRamp + '.colorEntryList[1].color', 1,0,0, type = 'double3')
    place2dTextureNode = cmds.shadingNode('place2dTexture', asUtility = True)
    cmds.connectAttr(place2dTextureNode + '.outUV', uRamp + '.uvCoord')
    cmds.connectAttr(place2dTextureNode + '.outUvFilterSize', uRamp + '.uvFilterSize')
    #create V Ramp
    vramp = cmds.shadingNode('ramp', asTexture = True)
    vRamp = cmds.rename(vramp, 'vRamp')
    cmds.setAttr(vRamp + '.type', 0)
    cmds.setAttr(vRamp + '.colorEntryList[0].color', 0,0,0, type = 'double3')
    cmds.setAttr(vRamp + '.colorEntryList[1].position', 1)
    cmds.setAttr(vRamp + '.colorEntryList[1].color', 0,1,0, type = 'double3')
    place2dTextureNode = cmds.shadingNode('place2dTexture', asUtility = True)
    cmds.connectAttr(place2dTextureNode + '.outUV', vRamp + '.uvCoord')
    cmds.connectAttr(place2dTextureNode + '.outUvFilterSize', vRamp + '.uvFilterSize')
    #Attach ramps to average node
    cmds.connectAttr(uRamp + '.outColor', plusNode + '.input3D[0]')
    cmds.connectAttr(vRamp + '.outColor', plusNode + '.input3D[1]')
 
    #connect the average node to UV element
    cmds.connectAttr(plusNode + '.output3D', uvPass + '.vray_texture_extratex')
 
#Create Rim Light Element
def createRim():
 
    rim = mel.eval('vrayAddRenderElement ExtraTexElement')
    #rename rim light element
    rimLight = cmds.rename(rim , 'rimLight')
    #set explicit channel name
    cmds.setAttr(rimLight + '.vray_explicit_name_extratex', 'rimLight', type = 'string')
    #Turn off affect matte Objects
    cmds.setAttr(rimLight + '.vray_affectmattes_extratex', 0)
 
    #Create Ramp and sampler info
    ramp = cmds.shadingNode('ramp', name = 'rimLight_ramp', asTexture = True)
    samplerInfo = cmds.shadingNode('samplerInfo', asUtility = True)
 
    #set ramp up
    cmds.setAttr(ramp + '.colorEntryList[2].position', .485)
    cmds.setAttr(ramp + '.colorEntryList[2].color', 0, 0, 0, type = 'double3')
    cmds.setAttr(ramp + '.colorEntryList[1].position', .100)
    cmds.setAttr(ramp + '.colorEntryList[1].color', .85, .8, .75, type = 'double3')
    cmds.setAttr(ramp + '.colorEntryList[0].position', 0)
    cmds.setAttr(ramp + '.colorEntryList[0].color', .94, .92, .9, type = 'double3')
 
    #connect sampler info to ramp
    cmds.connectAttr(samplerInfo + '.facingRatio', ramp + '.uCoord')
    cmds.connectAttr(samplerInfo + '.facingRatio', ramp + '.vCoord')
 
    #connect ramp to rimLight element
    cmds.connectAttr(ramp + '.outColor', rimLight + '.vray_texture_extratex')
 
#Create Position Pass Element
def createPPP():
 
    ppp = mel.eval('vrayAddRenderElement ExtraTexElement')
    #rename position pass element
    pppWorld = cmds.rename(ppp , 'pppWorld')
    #set explicit channel name
    cmds.setAttr(pppWorld + '.vray_explicit_name_extratex', 'pppWorld', type = 'string')
    #Turn off affect matte Objects
    cmds.setAttr(pppWorld + '.vray_affectmattes_extratex', 0)
 
    #create sampler info
    samplerInfoPPP = cmds.shadingNode('samplerInfo', asUtility = True)
 
    #connect sampler info to position pass element
    cmds.connectAttr(samplerInfoPPP + '.pointWorldX', pppWorld + '.vray_texture_extratexR')
    cmds.connectAttr(samplerInfoPPP + '.pointWorldY', pppWorld + '.vray_texture_extratexG')
    cmds.connectAttr(samplerInfoPPP + '.pointWorldZ', pppWorld + '.vray_texture_extratexB')
 
#Create Top Down Pass
def createTopDown():
 
    td = mel.eval('vrayAddRenderElement ExtraTexElement')
    #rename topdown element
    topDown = cmds.rename(td , 'TopDown')
    #set explicit channel name
    cmds.setAttr(topDown + '.vray_explicit_name_extratex', 'TopDown', type = 'string')
    #Turn off affect matte Objects
    cmds.setAttr(topDown + '.vray_affectmattes_extratex', 0)
 
    # now create the Falloff Tex Plugin import time
    tFalloffNode = mel.eval('vrayCreateNodeFromDll ("topdown_tex", "texture", "TexFalloff", 2);')
    #Set Attr for FalloffTex
    cmds.setAttr ('topdown_tex' + '.direction_type', 2)
    cmds.setAttr ('topdown_tex' + '.color1', 1, 0, 0, type='double3')
    cmds.setAttr ('topdown_tex' + '.color2', 0, 1, 0, type='double3')
 
    #connect to extra tex
    cmds.connectAttr ('topdown_tex' + '.outColor', topDown + '.vray_texture_extratex')
 
#Create Noise Pass
def createNoise():
 
    n = mel.eval('vrayAddRenderElement ExtraTexElement')
    #rename noise element
    noisePass = cmds.rename(n , 'Noise')
    #set explicit channel name
    cmds.setAttr(noisePass + '.vray_explicit_name_extratex', 'Noise', type = 'string')
 
    #create red fractal texture
    redFractal = cmds.shadingNode('fractal', name = 'redFractal', asTexture = True)
    #connect place2Dtexture node
    redPlace2dTextureNode = cmds.shadingNode('place2dTexture', asUtility = True)
    cmds.connectAttr(redPlace2dTextureNode + '.outUV' , redFractal + '.uvCoord')
    cmds.connectAttr(redPlace2dTextureNode + '.outUvFilterSize' , redFractal + '.uvFilterSize')
    #make red and smaller
    cmds.setAttr(redFractal + '.colorGain' , 1, 0, 0, type = 'double3')
    cmds.setAttr(redFractal + '.alphaIsLuminance', 1)
    cmds.setAttr(redPlace2dTextureNode + '.repeatU', 2)
    cmds.setAttr(redPlace2dTextureNode + '.repeatV', 2)
    #green fractal
    greenFractal = cmds.shadingNode('fractal', name = 'greenFractal', asTexture = True)
    #connect place2Dtexture node
    greenPlace2dTextureNode = cmds.shadingNode('place2dTexture', asUtility = True)
    cmds.connectAttr(greenPlace2dTextureNode + '.outUV' , greenFractal + '.uvCoord')
    cmds.connectAttr(greenPlace2dTextureNode + '.outUvFilterSize' , greenFractal + '.uvFilterSize')
    #make red and smaller
    cmds.setAttr(greenFractal + '.colorGain' , 0, 1, 0, type = 'double3')
    cmds.setAttr(greenFractal + '.alphaIsLuminance', 1)
    cmds.setAttr(greenPlace2dTextureNode + '.repeatU', .8)
    cmds.setAttr(greenPlace2dTextureNode + '.repeatV', .8)
    #blue fractal
    blueFractal = cmds.shadingNode('fractal', name = 'blueFractal', asTexture = True)
    #connect place2Dtexture node
    bluePlace2dTextureNode = cmds.shadingNode('place2dTexture', asUtility = True)
    cmds.connectAttr(bluePlace2dTextureNode + '.outUV' , blueFractal + '.uvCoord')
    cmds.connectAttr(bluePlace2dTextureNode + '.outUvFilterSize' , blueFractal + '.uvFilterSize')
    #make red and smaller
    cmds.setAttr(blueFractal + '.colorGain' , 0, 0, 1, type = 'double3')
    cmds.setAttr(blueFractal + '.alphaIsLuminance', 1)
    cmds.setAttr(bluePlace2dTextureNode + '.repeatU', 10)
    cmds.setAttr(bluePlace2dTextureNode + '.repeatV', 10)
    #create blendColors and connect three fractals
    blendColorsRG = cmds.shadingNode('blendColors', name = 'blendColorsRG', asUtility = True)
    cmds.connectAttr(redFractal + '.outColor' , blendColorsRG + '.color1')
    cmds.connectAttr(greenFractal + '.outColor' , blendColorsRG + '.color2')
    blendColorsRGB = cmds.shadingNode('blendColors', name = 'blendColorsRGB', asUtility = True)
    cmds.connectAttr(blendColorsRG + '.output' , blendColorsRGB + '.color1')
    cmds.connectAttr(blueFractal + '.outColor' , blendColorsRGB + '.color2')
 
    #connect to extra tex
    cmds.connectAttr ( blendColorsRGB + '.output', noisePass + '.vray_texture_extratex')   
 
#Create Wireframe Pass
 
def createWireframe():
 
    w = mel.eval('vrayAddRenderElement ExtraTexElement')
    #rename wireframe element
    wireframe = cmds.rename(w , 'Wireframe')
    #set explicit channel name
    cmds.setAttr(wireframe + '.vray_explicit_name_extratex', 'Wireframe', type = 'string')
    #create VRay Edge texture
    vEdge = cmds.shadingNode('VRayEdges', name = 'VRayEdges', asTexture = True)
    #connect place2Dtexture node
    place2dTextureNodeW = cmds.shadingNode('place2dTexture', asUtility = True)
    cmds.connectAttr(place2dTextureNodeW + '.outUV', vEdge + '.uvCoord')
    cmds.connectAttr(place2dTextureNodeW + '.outUvFilterSize', vEdge + '.uvFilterSize')
    #Set VRay edge pixels to .05
    cmds.setAttr(vEdge + '.pixelWidth', 0.05)
    #connect to extra tex
    cmds.connectAttr ( vEdge + '.outColor', wireframe + '.vray_texture_extratex')
 
def createCurvature():
    c = mel.eval('vrayAddRenderElement ExtraTexElement')
    #rename Curvature element
    curvature = cmds.rename(c , 'Curvature')
    #set explicit channel name
    cmds.setAttr(curvature + '.vray_explicit_name_extratex', 'Curvature', type = 'string')
    #Create VRay Curvature Node
    vCurv = cmds.shadingNode('VRayCurvature', name='VRayCurvature', asUtility = True)
    #Tweak default curvature settings
    cmds.setAttr(vCurv + '.subdivs', 8)
    cmds.setAttr(vCurv + '.sampleSpread', .7)
    cmds.setAttr(vCurv + '.scale', .1)
    #connect to extra tex
    cmds.connectAttr(vCurv + '.outColor' , curvature + '.vray_texture_extratex')  
 
#delete window if a window already exisits
if cmds.window('reWindow', exists=True):
    cmds.deleteUI('reWindow')
 
#Create my GUI
def createGUI():
    #window set up
    reWindow = cmds.window('reWindow',title="Custom Render Elements", rtf=True)
    cmds.columnLayout(adjustableColumn= True, rowSpacing= 3)
    cmds.checkBox('occlusionRE',label= "Occlusion", value=True)
    cmds.checkBox('fresnelRE', label= "Fresnel", value=True)
    cmds.checkBox('uvRE',label= "UV", value=True)
    cmds.checkBox('rimLightRE',label= "Rim Light", value=True)
    cmds.checkBox('worldPPPRE',label= "World PPP", value=True)
    cmds.checkBox('topDownRE',label= "Top Down", value=True)
    cmds.checkBox('noiseRE',label= "Noise", value=True)
    cmds.checkBox('wireframeRE',label= "Wireframe", value=True)
    cmds.checkBox('curvatureRE',label= "Curvature", value=True)
    cmds.button( label='Run', width= 224, command=('queryValues()'))
    cmds.setParent('..')
    cmds.setParent('..')
    cmds.showWindow('reWindow')
 
#query checkboxes
def queryValues():
 
    ocValue = cmds.checkBox('occlusionRE', query = True, value = True)
    frenValue = cmds.checkBox('fresnelRE', query = True, value = True)
    uvValue = cmds.checkBox('uvRE', query = True, value = True)
    rimValue = cmds.checkBox('rimLightRE', query = True, value = True)
    pppValue = cmds.checkBox('worldPPPRE', query = True, value = True)
    tdValue = cmds.checkBox('topDownRE', query = True, value = True)
    noiseValue = cmds.checkBox('noiseRE', query = True, value = True)
    wireframeValue= cmds.checkBox('wireframeRE', query = True, value = True)
    curvatureValue= cmds.checkBox('curvatureRE', query = True, value = True)
    #if query is true create the render element
    if ocValue == True:
        createOcc()
 
    if frenValue == True:
        createFresnel()
 
    if uvValue == True:
        createUv()
 
    if rimValue == True:
        createRim()
 
    if pppValue == True:
        createPPP()
 
    if tdValue == True:
        createTopDown()
 
    if noiseValue == True:
        createNoise()
 
    if wireframeValue == True:
        createWireframe()
 
    if curvatureValue == True:
       createCurvature()    
 
#Run the Script
createGUI()
