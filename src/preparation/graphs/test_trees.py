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

    print('-' * 100)
    root.pre_order_traversal()

    result = subj.inorder_succ(n4_5)
    assert result == root

    result = subj.inorder_succ(root)
    print(result)
    print(subj.inorder_succ(n2))


def test_build_dependencies():
    a, b, c, d, e, f = 'abcdef'
    projects = [a, b, c, d, e, f]
    # dependency = [(d, a), (b, f), (d, b), (a, f), (c, d)]
    dependencies = dict(
        d=[a, b],
        b=[f],
        a=[f],
        c=[d],
        e=[],
        f=[]
    )
    result = subj.build_dep(dependencies)
    print(result)
    expected = [e, f, b, a, d, c]
    print(result)
    assert expected == result


def test_build_dependencies_rises_error():
    a, b, c, d, e, f = 'abcdef'
    projects = [a, b, c, d, e, f]
    # dependency = [(d, a), (b, f), (d, b), (a, f), (c, d)]
    dependencies = dict(
        a=[b, e],
        b=[c],
        c=[a],
        e=[]
    )
    result = subj.build_dep(dependencies)
    print(result)
    # expected = [f, e, a, b, d, c]
    # assert expected == result


def test_find_common_parent():
    n0, n1, n2, n3, n4, n5, n6, n7, n8 = [subj.Node(i) for i in range(9)]
    root = n0
    root.left = n1
    n1.left = n2
    n1.right = n3
    n2.right = n4
    n3.left = n5
    result = subj.find_common_parent(root, n4, n5)
    print(result)
    assert n1 == result
    result = subj.common_ancestor(root, n4, n5)
    print(result)
    assert n1 == result


def test_get_initial_dataset():
    n0, n1, n2, n3, n4, n5, n6, n7, n8 = [subj.Node(i) for i in range(9)]

    root = n4
    root.left = n2
    root.right = n6
    n2.left = n1
    n2.right = n3
    n6.left = n5
    n6.right = n7
    result = subj.get_initial_dataset(root)
    expected = [
        [n4, n2, n6], [n4, n6, n2],
    ]

    assert result == expected


def test_is_sub_tree():
    n0, n1, n2, n3, n4, n5, n6, n7, n8 = [subj.Node(i) for i in range(9)]
    root = n4
    root.left = n2
    root.right = n6
    n2.left = n1
    n2.right = n3
    n1.left = n5
    n1.right = n7

    t2 = subj.Node(1)
    t2.left = subj.Node(5)
    t2.right = subj.Node(7)

    assert subj.is_sub_tree(root, t2) is True
    assert subj.is_sub_tree_2(root, t2) is True
    t2.right.left = n0
    assert subj.is_sub_tree(root, t2) is False
    assert subj.is_sub_tree_2(root, t2) is False
