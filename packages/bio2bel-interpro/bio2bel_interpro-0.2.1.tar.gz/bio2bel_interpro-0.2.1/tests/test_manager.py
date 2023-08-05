# -*- coding: utf-8 -*-

"""This module tests that proteins in a given BELGraph can be annotated to their families.

This file does NOT test the existence of the InterPro hierarchy.
"""

import unittest

from pybel import BELGraph
from pybel.constants import IS_A, RELATION
from pybel.dsl import protein
from tests.cases import TemporaryCacheClassMixin

mapk1_hgnc = protein(namespace='hgnc', name='MAPK1', identifier='6871')
mapk1_uniprot = protein(namespace='uniprot', name='MK01_HUMAN', identifier='P28482')

interpro_identifiers = [
    'IPR011009',  # . Kinase-like_dom.
    'IPR003527',  # . MAP_kinase_CS.
    'IPR008349',  # . MAPK_ERK1/2.
    'IPR000719',  # . Prot_kinase_dom.
    'IPR017441',  # . Protein_kinase_ATP_BS.
    'IPR008271',  # . Ser/Thr_kinase_AS.
]

interpro_family_nodes = [
    protein(
        namespace='interpro',
        identifier=identifier,
    )
    for identifier in interpro_identifiers
]


class TestManager(TemporaryCacheClassMixin):
    """Tests the enrichment functions of the manager are working properly."""

    def test_populated(self):
        """Test the database was populated and can be queried."""
        result = self.manager.get_interpro_by_name('Ubiquitin/SUMO-activating enzyme E1')
        self.assertIsNotNone(result)

        child = self.manager.get_interpro_by_name('Ubiquitin-activating enzyme E1')
        self.assertIsNotNone(child)

        self.assertEqual(result.interpro_id, 'IPR000011')
        self.assertEqual(len(result.children), 1)
        self.assertIn(child, result.children)

    @unittest.skip
    def test_enrich_uniprot(self):
        """Test enriching UniProt entries."""
        graph = BELGraph()
        graph.add_node_from_data(mapk1_uniprot)

        self.assertEqual(1, graph.number_of_nodes())
        self.assertEqual(0, graph.number_of_edges())

        self.manager.enrich_proteins(graph)

        for interpro_family_node in interpro_family_nodes:
            self.assertIn(interpro_family_node, graph)
            self.assertIn(interpro_family_node, graph[mapk1_uniprot])
            v = list(graph[mapk1_uniprot][interpro_family_node].values())[0]
            self.assertIn(RELATION, v)
            self.assertEqual(IS_A, v[RELATION])

    @unittest.skip
    def test_enrich_hgnc(self):
        """Test that the enrich_proteins function gets the interpro entries in the graph."""
        graph = BELGraph()
        graph.add_node_from_data(mapk1_hgnc)

        self.assertEqual(1, graph.number_of_nodes())
        self.assertEqual(0, graph.number_of_edges())

        self.manager.enrich_proteins(graph)

        for interpro_family_node in interpro_family_nodes:
            self.assertIn(interpro_family_node, graph)
            self.assertIn(interpro_family_node, graph[mapk1_hgnc])
            v = list(graph[mapk1_hgnc][interpro_family_node].values())[0]
            self.assertIn(RELATION, v)
            self.assertEqual(IS_A, v[RELATION])
