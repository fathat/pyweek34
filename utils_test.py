import unittest
from panda3d.core import Plane, LVector3f, LPoint3f
from utils import triangle_plane_intersection

class test_triangle_intersection(unittest.TestCase):
    def setUp(self):
        self.plane = Plane(LVector3f(0, -1, 0), LPoint3f(0, 0, 0))

    def test_simple_intersection(self):
        """
        In this test case, the plane passes through the origin and faces towards the camera

        (z is up and y is depth)

        The triangle is flat on the xz plane and crosses at -2.5, 0, 0 and 2.5, 0, 0
        """
        triangle = [
            LPoint3f( 5, -5, 0),
            LPoint3f(-5, -5, 0),
            LPoint3f( 0,  5, 0)
        ]

        intersection = triangle_plane_intersection(triangle, self.plane)
        assert(len(intersection) == 2)

    def test_triangle_on_plane(self):
        """In this test case, the entire triangle lies on the plane. So we should get three points back"""
        triangle = [
            LPoint3f( 5, 0, -5),
            LPoint3f(-5, 0, -5),
            LPoint3f( 0, 0,  5)
        ]

        intersection = triangle_plane_intersection(triangle, self.plane)
        assert(len(intersection) == 3)
        
    def test_triangle_edge_on_plane(self):
        """In this test case, one edge of the triangle lies on the plane, so we should get that edge back"""
        triangle = [
            LPoint3f( 5, 0, 0),
            LPoint3f(-5, 0, 0),
            LPoint3f( 0, -5, 0)
        ]

        intersection = triangle_plane_intersection(triangle, self.plane)
        assert(len(intersection) == 2)