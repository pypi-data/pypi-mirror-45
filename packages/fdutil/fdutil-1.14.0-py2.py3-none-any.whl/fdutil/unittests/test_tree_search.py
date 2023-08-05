# encoding: utf-8

import unittest

from fdutil.tree_search import TreeSearch


def uppercase_fields(node,
                     fields,
                     **_):
    for field in fields:
        try:
            node[field] = node[field].upper()
        except KeyError:
            pass


class TestTreeSearch(unittest.TestCase):

    TEST_DICT = {"cmsid": "UKPR085589CAC7",
                 "childnodes": [{"t": "Rail 1",
                                 "childnodes": [{"t": "item 1", "sy": "rail 1 item 1"},
                                                {"t": "item 2", "sy": "rail 1 item 2"},
                                                {"t": "item 3", "sy": "rail 1 item 3"},
                                                {"t": "item 4", "sy": "rail 1 item 4"},
                                                {"t": "item 5", "sy": "rail 1 item 5"},
                                               ],
                                 },
                                {"t": "Rail 2",
                                 "childnodes": [{"t": "item 1", "sy": "rail 2 item 1"},
                                                {"t": "item 2", "sy": "rail 2 item 2"},
                                                {"t": "item 3", "sy": "rail 2 item 3"},
                                                {"t": "item 4", "sy": "rail 2 item 4"},
                                                ],
                                 },
                                {"t": "Rail 3",
                                 "childnodes": [{"t": "item 1", "sy": "rail 3 item 1"},
                                                {"t": "item 2", "sy": "rail 3 item 2"},
                                                {"t": "item 3", "sy": "rail 3 item 3"},
                                               ],
                                 },
                                ],
                 }

    def setUp(self):
        self.ts = TreeSearch(default_key='t',
                             zero_index=False)
        self.ts_zero_index = TreeSearch(default_key='t')

    def tearDown(self):
        pass

    # is_dictionary
    def test_1_level_deep(self):
        matched_nodes = self.ts.search(tree=self.TEST_DICT,
                                       path=["childnodes"])

        assert len(matched_nodes) == 3

    def test_2_levels_deep(self):
        matched_nodes = self.ts.search(tree=self.TEST_DICT,
                                       path=["childnodes", "Rail 1"])

        assert len(matched_nodes) == 1
        assert matched_nodes[0].get('t') == "Rail 1"

    def test_3_levels_deep(self):
        matched_nodes = self.ts.search(tree=self.TEST_DICT,
                                       path=["childnodes", "Rail 1", "childnodes"])

        assert len(matched_nodes) == 5
        assert isinstance(matched_nodes[0], dict)
        assert matched_nodes[0]['sy'] == "rail 1 item 1"
        assert matched_nodes[-1]['sy'] == "rail 1 item 5"

    def test_3_levels_deep_with_index(self):
        matched_nodes = self.ts.search(tree=self.TEST_DICT,
                                       path=["childnodes", 2, "childnodes"], )

        assert len(matched_nodes) == 4
        assert isinstance(matched_nodes[0], dict)
        assert matched_nodes[0]['sy'] == "rail 2 item 1"
        assert matched_nodes[-1]['sy'] == "rail 2 item 4"

    def test_0_index_3_levels_deep_with_index(self):
        matched_nodes = self.ts_zero_index.search(tree=self.TEST_DICT,
                                                  path=["childnodes", 1, "childnodes"], )

        assert len(matched_nodes) == 4
        assert isinstance(matched_nodes[0], dict)
        assert matched_nodes[0]['sy'] == "rail 2 item 1"
        assert matched_nodes[-1]['sy'] == "rail 2 item 4"

    def test_3_levels_deep_with_implicit_full_list(self):
        matched_nodes = self.ts.search(tree=self.TEST_DICT,
                                       path=["childnodes", "childnodes"])

        assert len(matched_nodes) == 12
        assert isinstance(matched_nodes[0], dict)
        assert matched_nodes[0]['sy'] == "rail 1 item 1"
        assert matched_nodes[-1]['sy'] == "rail 3 item 3"

    def test_3_levels_deep_with_implicit_full_list_and_index(self):
        matched_nodes = self.ts.search(tree=self.TEST_DICT,
                                       path=["childnodes", "childnodes", 2])

        assert len(matched_nodes) == 3
        assert isinstance(matched_nodes[0], dict)
        assert matched_nodes[0]['sy'] == "rail 1 item 2"
        assert matched_nodes[1]['sy'] == "rail 2 item 2"
        assert matched_nodes[2]['sy'] == "rail 3 item 2"

    def test_0_index_3_levels_deep_with_implicit_full_list_and_index(self):
        matched_nodes = self.ts_zero_index.search(tree=self.TEST_DICT,
                                                  path=["childnodes", "childnodes", 1])

        assert len(matched_nodes) == 3
        assert isinstance(matched_nodes[0], dict)
        assert matched_nodes[0]['sy'] == "rail 1 item 2"
        assert matched_nodes[1]['sy'] == "rail 2 item 2"
        assert matched_nodes[2]['sy'] == "rail 3 item 2"

    def test_3_levels_deep_with_implicit_full_list_and_default_key_match(self):
        matched_nodes = self.ts.search(tree=self.TEST_DICT,
                                       path=["childnodes", "childnodes", "item 3"])

        assert len(matched_nodes) == 3
        assert isinstance(matched_nodes[0], dict)
        assert matched_nodes[0]['sy'] == "rail 1 item 3"
        assert matched_nodes[1]['sy'] == "rail 2 item 3"
        assert matched_nodes[2]['sy'] == "rail 3 item 3"

    def test_3_levels_deep_with_implicit_full_list_and_explicit_key_match(self):
        matched_nodes = self.ts.search(tree=self.TEST_DICT,
                                       path=["childnodes", "childnodes", {"sy": "rail 1 item 4"}])

        assert len(matched_nodes) == 1
        assert isinstance(matched_nodes[0], dict)
        assert matched_nodes[0]['sy'] == "rail 1 item 4"
        assert matched_nodes[0]['t'] == "item 4"

    def test_apply_uppercase_fields(self):
        assert self.TEST_DICT['childnodes'][0]['childnodes'][3]['t'] == "item 4"
        assert self.TEST_DICT['childnodes'][0]['childnodes'][3]['sy'] == "rail 1 item 4"

        self.ts.apply_func_at_path(tree=self.TEST_DICT,
                                   path=["childnodes", "childnodes", {"sy": "rail 1 item 4"}],
                                   func=uppercase_fields,
                                   fields=["sy", "t"])

        assert self.TEST_DICT['childnodes'][0]['childnodes'][3]['t'] == "ITEM 4"
        assert self.TEST_DICT['childnodes'][0]['childnodes'][3]['sy'] == "RAIL 1 ITEM 4"

