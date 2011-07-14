
import unittest
import core

class CreateProject(unittest.TestCase):
    def setUp(self):
        p = core.Project()
        p.add_parameter("var1", 10, (0, 100))
        p.add_parameter("var2", 20, (10, 88))
        p.add_constraint("con1", (0, 10))
        p.add_constraint("con2", (None, 5))
        p.add_objective("obj1")
        p.add_objective("obj2")
        self.Project = p

    def tearDown(self):
        self.Project = None

    def test_add_parameters(self):
        p = self.Project
        # order must be preserved
        self.assertEquals(p.get_parameter_names(), ["var1", "var2"])
        self.assertEquals(p.get_parameter_default_values(), [10, 20])
        self.assertEquals(p.get_parameter_ranges(), [(0,100), (10,88)])
        # setting an invalid default value
        self.assertRaises(core.DefaultValueOutOfRange, 
            self.Project.add_parameter, "var3", 0, (10,100)) 
        # make sure the invalid parameter doesn't get added
        self.assertEquals(len(self.Project.get_parameter_names()), 2)

    def test_add_constraints(self):
        p = self.Project
        # order must be preserved
        self.assertEquals(p.get_constraint_names(), ["con1", "con2"])
        self.assertEquals(p.get_constraint_bounds(), [(0,10), (None,5)])

    def test_add_objectives(self):
        p = self.Project
        self.assertEquals(p.get_objective_names(), ["obj1", "obj2"])

    def test_read_and_write_project(self):
        data = self.Project.to_json()
        self.Project.from_json(data)
        data2 = self.Project.to_json()
        self.assertEquals(data, data2)

    def test_read_and_write_empty_project(self):
        p = core.Project()
        data = p.to_json()
        p.from_json(data)
        data2 = p.to_json()
        self.assertEquals(data, data2)
        

if __name__ == "__main__":
    unittest.main()


