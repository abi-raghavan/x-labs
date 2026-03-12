import hashlib


def assign_variant(user_id, experiment_id, split):
    hash_input = f"{user_id}_{experiment_id}"
    hash_value = int(hashlib.sha256(hash_input.encode()).hexdigest(), 16)
    return "control" if (hash_value % 100) < (split * 100) else "variant"