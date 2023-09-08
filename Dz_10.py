import maya.cmds as cmds
import maya.OpenMaya as OpenMaya


def main():
    try:
        selection = cmds.ls(sl=1, l=1)[0]
    except:
        print("Select object")
        return
    selection_list = OpenMaya.MSelectionList()
    selection_list.add(selection)

    mDagPath = OpenMaya.MDagPath()
    selection_list.getDagPath(0, mDagPath)
    fnMesh = OpenMaya.MFnMesh(mDagPath)

    eIter = OpenMaya.MItMeshEdge(mDagPath)

    while not eIter.isDone():
        vertID_A = eIter.index(0)
        vertID_B = eIter.index(1)

        pos_A = OpenMaya.MPoint()
        pos_B = OpenMaya.MPoint()

        fnMesh.getPoint(vertID_A, pos_A, OpenMaya.MSpace.kWorld)
        fnMesh.getPoint(vertID_B, pos_B, OpenMaya.MSpace.kWorld)

        name_curve = cmds.curve(d=1, p=[(pos_A.x, pos_A.y, pos_A.z), (pos_B.x, pos_B.y, pos_B.z)], k=[0, 1])
        tangents = cmds.pointOnCurve(name_curve, p=0, normalizedTangent=1)
        circle = cmds.circle(nr=(tangents[0], tangents[1], tangents[2]), c=(0, 0, 0), sw=360, r=0.1)[0]

        cmds.xform(circle, t=[pos_B.x, pos_B.y, pos_B.z], ws=1)
        cmds.extrude(circle, name_curve, rn=0, po=0, et=2, ucp=0, fpt=1, upn=1, rotation=0, scale=1, rsp=1, ch=0)

        eIter.next()


main()
