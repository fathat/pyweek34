import pymunk
from pymunk import Vec2d
from panda3d.core import GeomVertexReader, Plane, LVector3f, LPoint3f, LineSegs, NodePath
from typing import List

import masks
import utils


def process_geom_node(geomNode):
    assert(geomNode.checkValid())
    triangles = []
    for i in range(geomNode.getNumGeoms()):
        geom = geomNode.getGeom(i)
        state = geomNode.getGeomState(i)
        triangles.extend(process_geom(geom))
    return triangles


def process_geom(geom):
    vdata = geom.getVertexData()
    triangles = []
    for i in range(geom.getNumPrimitives()):
        prim = geom.getPrimitive(i)
        #print(prim)
        triangles.extend(process_primitive(prim, vdata))
    return triangles


def process_primitive(prim, vdata):
    vertex = GeomVertexReader(vdata, 'vertex')

    # decompose so we only have to worry about dealing with triangles
    prim = prim.decompose()

    triangles = []
    for p in range(prim.getNumPrimitives()):
        s = prim.getPrimitiveStart(p)
        e = prim.getPrimitiveEnd(p)
        triangle = []
        for i in range(s, e):
            vi = prim.getVertex(i)
            vertex.setRow(vi)
            v = vertex.getData3()
            triangle.append(v)
            #print("prim %s has vertex %s: %s" % (p, vi, repr(v)))
        triangles.append(triangle)
    return triangles


def process_vertex_data(vdata):
    vertex = GeomVertexReader(vdata, 'vertex')
    texcoord = GeomVertexReader(vdata, 'texcoord')
    while not vertex.isAtEnd():
        v = vertex.getData3()
        t = texcoord.getData2()
        print("v = %s, t = %s" % (repr(v), repr(t)))

class Wall:
    def __init__(self):
        self.shape = None

def create_segments(transformed_triangle, physics_plane, space, render):
    segments = utils.triangle_plane_intersection(transformed_triangle, physics_plane)
    if segments and len(segments) > 1: 
        if len(segments) > 2:
            print("more than two segments, there may be issues")
        for i in range(len(segments)-1):
            p1 = segments[i].getXz()
            p2 = segments[i+1].getXz()
            shape = pymunk.Segment(space.static_body, Vec2d(*p1), Vec2d(*p2), 0.0)
            shape.friction = 1.0
            shape.collision_type = masks.CATEGORY_WALL
            shape.filter = pymunk.ShapeFilter(categories=masks.CATEGORY_WALL)
            
            temp = Wall()
            temp.shape = shape
            shape.data = temp
            space.add(shape)

            if render:
                lines = LineSegs()
                lines.setColor(1, 0, 0, 1)
                lines.moveTo(p1[0], 0, p1[1])
                lines.drawTo(p2[0], 0, p2[1])
                lines.setThickness(4)
                node = lines.create()
                np = NodePath(node)
                np.reparentTo(render)


def add_node_path_as_collider(node_path, space, render=None):
    physics_plane = Plane(LVector3f(0, -1, 0), LPoint3f(0, 0, 0))
    geom_node_collection = node_path.findAllMatches('**/+GeomNode')
    for geom_node_path in geom_node_collection:
        geom_node = geom_node_path.node()
        mat4 = geom_node_path.getNetPrevTransform().getMat()
        triangles = process_geom_node(geom_node)
        for triangle in triangles:
            # triangle is in local space, so bring it to world space of node_path
            transformed_triangle = [mat4.xformPoint(p) for p in triangle]
            create_segments(transformed_triangle, physics_plane, space, render)
