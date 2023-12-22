import sys
sys.path.append('./')
from structs.graph import Graph
import unittest

class GraphTest(unittest.TestCase):
    """unit tests for the Graph class using the Arrange, Act, Assert (AAA) method"""
    
    def test_add_edge(self):
        """expect None when attempted edge duplicate insertion, original graph not altered"""

        g = Graph()
        edges = [("london", "rome"), ("london", "lisbon"), ("rome", "london"), ("lisbon", "rome"), ("rome", "berlin")]
        for edge in edges:
            source, target = edge[0], edge[1]
            g.add_edge(source, target)
        
        self.assertEqual(g.add_edge("rome", "london"), None)

    def test_path_exists(self):
        """expect True if path exists, otherwise False"""
        
        g = Graph()
        edges = [("london", "rome"), ("london", "lisbon"), ("rome", "london"), ("lisbon", "rome"), ("rome", "berlin")]
        for edge in edges:
            source, target = edge[0], edge[1]
            g.add_edge(source, target)

        self.assertTrue(g.path_exists("london", "berlin"))

    def test_all_reachables(self):
        """expect array with all nodes reachable for source node in order discovered during BFS"""

        g = Graph()
        edges = [("london", "rome"), ("london", "lisbon"), ("rome", "london"), ("lisbon", "rome"), ("rome", "berlin")]
        for edge in edges:
            source, target = edge[0], edge[1]
            g.add_edge(source, target)

        self.assertEqual(g.all_reachables("london"), ['rome', 'lisbon'])
        self.assertEqual(g.all_reachables("lisbon"), ['london', 'rome'])

    def test_get_vertices(self):
        """expect array with all vertices present in the graph"""

        g = Graph()
        edges = [("london", "rome"), ("london", "lisbon"), ("rome", "london"), ("lisbon", "rome"), ("rome", "berlin")]
        for edge in edges:
            source, target = edge[0], edge[1]
            g.add_edge(source, target)
        
        self.assertEqual(g.get_vertices(), ['london', 'rome', 'lisbon'])

if __name__ == "__main__":
    unittest.main()