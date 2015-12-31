import unittest
import Swoop
import Swoop.ext.ShapelySwoop
from Swoop.ext.ShapelySwoop import ShapelyEagleFilePart as SEFP
import os
import shapely
import re
from Swoop.ext.ShapelySwoop import GeometryDump as GeoDump
from Swoop.ext.ShapelySwoop import ShapelySwoop as ShapelySwoop

def hash_geo(geo):
    """
    Hash a shapley geometry object by converting it to string, rounding all the floats it contains and taking a hash of the resulting string.  
    
    The rounding prevents false failures due to floating point errors.
    """
    def trim(match):
        return str(round(float(match.group(0)), 5))
    v = re.sub("-?\d+(\.\d+)?", trim, str(geo))
    return hash(v)

def dump(test, geo, title, c, color):
    hash = hash_geo(geo)
    print """("{}", {}, "{}"),""".format(test[0], hash, test[2])
    Swoop.ext.ShapelySwoop.dump_geometry(geo, "{} ({})".format(title,hash) , "{0:03d}.pdf".format(c), color)


class TestShapely(unittest.TestCase):
    
    def setUp(self):
        self.me = os.path.dirname(os.path.realpath(__file__))
        self.testbrd1 = ShapelySwoop.from_file(self.me + "/inputs/shapeTest1.brd")
        self.testbrd2 = ShapelySwoop.from_file(self.me + "/inputs/shapeTest2.brd")
        self.testbrd3 = ShapelySwoop.from_file(self.me + "/inputs/shapeTest3.brd")

        self.boardtest = ShapelySwoop.from_file(self.me + "/inputs/test_saving.brd")
        
    def test_element(self):
        tests = [
            ("shapely.ops.cascaded_union(Swoop.From(self.testbrd1).get_elements().get_geometry())", 4543782496711782003, "#000000"),
            ("self.testbrd1.get_element('U$1').get_geometry()", 558293734914727651, "#000000"),
            ("self.testbrd1.get_element('U$2').get_geometry()", 1542196656777319817, "#000000"),
            ("self.testbrd1.get_element('U$2').get_geometry(layer_query='Top')", -2316119240083132091, "#ff0000"),
            ("shapely.ops.cascaded_union(Swoop.From(self.testbrd1).get_elements().get_geometry(layer_query='Top'))", -1405743727263307022, "#ff0000"),
            ("shapely.ops.cascaded_union(Swoop.From(self.testbrd2).get_elements().get_geometry())", 1383575516265791664, "#000000"),
            ("shapely.ops.cascaded_union(Swoop.From(self.testbrd2).get_elements().get_geometry(layer_query='tPlace'))", 4675948399285872422, "#000000"),
            ("shapely.ops.cascaded_union(Swoop.From(self.testbrd2).get_elements().get_geometry(layer_query='bPlace'))", -8147871516156910189, "#000000"),
            ("shapely.ops.cascaded_union(Swoop.From(self.testbrd2).get_element('U$1').get_geometry(layer_query='Top'))", -5301026454227315084, "#ff0000"),
            ("shapely.ops.cascaded_union(Swoop.From(self.testbrd2).get_element('U$1').get_geometry(layer_query='Bottom'))", -5999577188847035307, "#0000ff"),
            ("shapely.ops.cascaded_union(Swoop.From(self.testbrd2).get_elements().get_geometry(layer_query='tTest2'))", -8049353574747205132, "#ff00ff"),
            ("shapely.ops.cascaded_union(Swoop.From(self.testbrd2).get_elements().get_geometry(layer_query='bTest2'))", 3934649351525441535, "#ff00ff"),
            ("shapely.ops.cascaded_union(self.boardtest.get_geometry())", 6722318116014407667, "#000000"),
            ("shapely.ops.cascaded_union(Swoop.From(self.testbrd2).get_elements().get_geometry(layer_query='Holes'))", 7701255143946384531, "#000000"),
            ("shapely.ops.cascaded_union(Swoop.From(self.testbrd2).get_elements().get_geometry(layer_query='tKeepout', polygonize_wires=SEFP.POLYGONIZE_BEST_EFFORT))", -5168448055214345009, "#000000"),
            ("shapely.ops.cascaded_union(Swoop.From(self.testbrd2).get_elements().get_geometry(layer_query='tKeepout', polygonize_wires=SEFP.POLYGONIZE_NONE))", -6142800795751873055, "#000000"),
        ]

        c = 0
        # We compare the geometry the commands produced with a hash of the
        # correct geometry.  If you need to update the correct answers,
        # uncomment the "dump" below, and comment out the assert.  Run
        # "frameworkpython -m unittest test_Shapely.TestShapely.test_element"
        # and then look at all ???.pdf files.  Check that they correct.  When
        # they are replace the array above with the output of the command.
        # It's the commands with the updated hashes.  Questions? ask Steve.
        for i in tests:
            geo = eval(i[0])
            #dump(i, geo, i[0], c, i[2])
            self.assertEqual(hash_geo(geo), i[1], "Geometry failure on test {}".format(c))
            c = c + 1
