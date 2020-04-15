import preparation.graphs.tasks as subj


def test_is_balanced():
    n = subj.Node(20)
    n.left = subj.Node(10)
    n.right = subj.Node(30)
    n.right.right = subj.Node(40)
    n.right.right.right = subj.Node(50)
    n.pre_order_traversal()

    assert subj.is_balanced(n) is False
    assert subj.is_balanced_2(n) is False

    n.left.right = subj.Node(11)
    n.right.left = subj.Node(25)
    n.pre_order_traversal()

    assert subj.is_balanced(n) is True
    assert subj.is_balanced_2(n) is True


def test_is_binary_search_tree():
    root = subj.Node(10)
    assert subj.is_binary_search_tree(root) is True

    n20 = subj.Node(20)
    n5 = subj.Node(5)
    root.left = n20
    assert subj.is_binary_search_tree(root) is False
    root.left = None
    root.right = n5
    assert subj.is_binary_search_tree(root) is False
    assert subj.check_bst(root) is False

    root.left = n5
    root.right = n20
    assert subj.is_binary_search_tree(root) is True
    assert subj.is_binary_search_tree_2(root) is True
    assert subj.check_bst(root) is True

    n5.right = subj.Node(30)

    assert subj.is_binary_search_tree(root) is False
    assert subj.is_binary_search_tree_2(root) is False
    assert subj.check_bst(root) is False
    print()
    root.pre_order_traversal()
    n5.right = None
    n5.right = subj.Node(10)

    print()
    root.pre_order_traversal()
    assert subj.is_binary_search_tree(root) is False
    assert subj.is_binary_search_tree_2(root) is False
    assert subj.check_bst(root) is False

