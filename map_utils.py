import os


def walk_branches(node, handle_item):
    for key, item in node.iteritems():
        result = handle_item(key, item)
        if result:
            return result
        if isinstance(item, dict):
            result = walk_branches(item, handle_item)
            if result:
                return result

    return None


def validate(groups_map, group_scenarios):
    group_names = list()
    error_list = list()

    def _validate_node(key, item):
        leaf_group_name = None
        if item is None:
            leaf_group_name = key

        elif isinstance(item, str):
            leaf_group_name = item

        if leaf_group_name and not group_scenarios.get(leaf_group_name):
            error_list.append('error: leaf group "{}" has no scenarios!'.format(leaf_group_name))

        group_name = leaf_group_name if leaf_group_name else key
        if group_name in group_names:
            error_list.append('error: group name "{}" found more than once in a groups map'.format(group_name))

        else:
            group_names.append(group_name)

        if not leaf_group_name and not group_scenarios.get(group_name):
            for subgroup_name in item.keys():
                if not group_scenarios.get(subgroup_name):
                    print('warning: group {} and subgroup {} '
                          'do not have any scenarios both'.format(group_name, subgroup_name))

    walk_branches(groups_map, _validate_node)

    if error_list:
        raise Exception(''.join([os.linesep + error for error in error_list]))
