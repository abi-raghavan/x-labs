from retrieve import reciprocal_rank_fusion, recall_at_k


def test_reciprocal_rank_fusion():
    # fixtures
    rank_lists = [
        ["a", "b", "c"],
        ["b", "d", "a"],
    ]
    expected = ["b", "a", "d", "c"]

    # run
    result = reciprocal_rank_fusion(rank_lists, k=60)

    # assert
    assert result == expected


def test_recall_at_k_hit():
    # fixtures
    retrieved_ids = ["x", "y", "z", "a", "b"]
    gold_ids = ["a"]
    expected = True

    # run
    result = recall_at_k(retrieved_ids, gold_ids, 5)

    # assert
    assert result == expected


def test_recall_at_k_miss():
    # fixtures
    retrieved_ids = ["x", "y", "z"]
    gold_ids = ["a"]
    expected = False

    # run
    result = recall_at_k(retrieved_ids, gold_ids, 3)

    # assert
    assert result == expected
