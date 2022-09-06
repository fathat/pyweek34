import pymunk
from panda3d.core import GeomVertexReader, Plane, LVector3f, LPoint3f, LineSegs, NodePath
from pymunk import Vec2d

import utils


def process_geom_node(geomNode):
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


def add_node_path_as_collider(node, node_path, space, render=None):
    physics_plane = Plane(LVector3f(0, -1, 0), LPoint3f(0, 0, 0))

    mat4 = node_path.getTransform().getMat()
    geom_node_collection = node.findAllMatches('**/+GeomNode')
    for nodePath in geom_node_collection:
        geom_node = nodePath.node()
        triangles = process_geom_node(geom_node)
        for triangle in triangles:
            # triangle is in local space, so bring it to world space of node_path
            transformed_triangle = [mat4.xformPoint(p) for p in triangle]
            segments = utils.triangle_plane_intersection(transformed_triangle, physics_plane)
            if segments and len(segments) == 2: # TODO: handle rare case of 3 segments
                p1 = segments[0].getXz()
                p2 = segments[1].getXz()
                shape = pymunk.Segment(space.static_body, Vec2d(*p1), Vec2d(*p2), 0.0)
                shape.friction = 1.0
                shape.filter = pymunk.ShapeFilter(categories=utils.CATEGORY_WALL)
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
