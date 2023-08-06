"""
helper functions for unit tests
"""

def full_path(root: str, file_name: str, sub_dir: str = None) -> str:
    """
    helper function to return a full
    path instead of writing formatted strs
    """
    if sub_dir is not None:
        return '{}/{}/{}'.format(root, sub_dir, file_name)
    return '{}/{}'.format(root, file_name)
