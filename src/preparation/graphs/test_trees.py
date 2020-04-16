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
    assert subj.check_bst_2(root) is True

    n5.right = subj.Node(30)

    assert subj.is_binary_search_tree(root) is False
    assert subj.is_binary_search_tree_2(root) is False
    assert subj.check_bst(root) is False
    assert subj.check_bst_2(root) is False

    print()
    root.pre_order_traversal()
    n5.right = None
    n5.right = subj.Node(10)

    print()
    root.pre_order_traversal()
    assert subj.is_binary_search_tree(root) is False
    assert subj.is_binary_search_tree_2(root) is False
    assert subj.check_bst(root) is False
    assert subj.check_bst_2(root) is False


def test_get_next():
    root = subj.Node(10)
    assert subj.get_next(root) is None

    n20 = subj.Node(20)
    n3 = subj.Node(3)
    root.add('left', n3)
    root.add('right', n20)
    assert subj.get_next(n3) == n20

    n2 = subj.Node(2)
    root.left.add('left', n2)

    n11 = subj.Node(11)
    root.right.add('left', n11)

    assert subj.get_next(n2) == n11

    n20.left = None
    assert subj.get_next(n2) == n20

    n20.add('left', n11)
    n10_5 = subj.Node(10.5)
    n11.add('left', n10_5)
    n10_5.add('left', subj.Node(10.4))
    n4 = subj.Node(4)
    n3.add('right', n4)
    n4.add('left', subj.Node(3))
    n4_5 = subj.Node(4.5)
    n4.add('right', n4_5)
    # root.pre_order_traversal()

    result = subj.get_next(n4_5)
    assert result == n10_5

    print('-'*100)
    root.pre_order_traversal()

    result = subj.inorder_succ(n4_5)
    assert result == root

    result = subj.inorder_succ(root)
    print(result)
    print('-'*100)
    subj.symentrical_order(root)
    print(subj.inorder_succ(n2))
