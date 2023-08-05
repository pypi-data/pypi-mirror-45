# encoding: utf-8


class TreeSearch(object):

    def __init__(self,
                 default_key=None,
                 case_sensitive=False,
                 zero_index=True):
        self.default_key = default_key
        self.case_sensitive = case_sensitive
        self.index_adjustment = 0 if zero_index else 1

    def dict_match(self,
                   obj,
                   match_dict):
        """
        Check that a dictionary matches
        :param obj:
        :param match_dict:
        :return: Boolean
        """
        for key, value in match_dict.items():
            try:
                actual_value = obj[key]
            except (KeyError, TypeError):
                return False  # object doesn't have the key

            match_value = value

            if not self.case_sensitive:
                try:
                    actual_value = actual_value.lower()
                except AttributeError:
                    pass

                try:
                    match_value = match_value.lower()
                except AttributeError:
                    pass

            if actual_value != match_value:
                return False

        return True

    def search(self,
               tree,
               path):
        """
        Looks through the tree matching value, keys and array indices.
        When selecting from childnodes, you need to give the title.

        :param tree: a dict or list
        :param path: a list dictionary keys, indices or key value pairs
        :return: matching nodes


        """

        if isinstance(tree, list):

            if isinstance(path[0], int):  # Get single index item from list
                try:
                    match = tree[path[0] - self.index_adjustment]

                    if len(path) > 1:
                        return self.search(tree=match,
                                           path=path[1:])
                    else:
                        return [match]

                except IndexError:
                    return []  # No match
            else:
                # It's a list, match each element separately
                matches = []
                for node in tree:
                    matched = self.search(tree=node,
                                          path=path)
                    if isinstance(matched, list):
                        matches.extend(matched)
                    else:
                        matches.append(matched)
                return [m for m in matches if m]

        else:
            # Not a list !
            try:
                match = tree[path[0]]
                if len(path) > 1:
                    matches = self.search(tree=match,
                                          path=path[1:])
                    return matches
                else:
                    return match if isinstance(match, list) else [match]
            except (KeyError, TypeError):
                pass

            try:
                if isinstance(path[0], dict):
                    match_dict = path[0]
                elif self.default_key is not None:
                    match_dict = {self.default_key: path[0]}
                else:
                    raise ValueError(u'default_ky has been configured')

                if self.dict_match(obj=tree, match_dict=match_dict):
                    if len(path) > 1:
                        matches = self.search(tree=tree,
                                              path=path[1:])
                        return matches
                    else:
                        return tree

            except AttributeError:
                pass

    def apply_func_at_path(self,
                           tree,
                           path,
                           func,
                           **params):

        nodes = self.search(tree=tree,
                            path=path)
        for node in nodes:
            try:
                func(node=node,
                     **params)
            except TypeError:
                raise ValueError(u'Bad params for {func}: {params}'
                                 .format(func=func,
                                         params=params))
