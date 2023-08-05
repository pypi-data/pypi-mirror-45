import os
from typing import List, Optional

from unidiff import PatchSet, PatchedFile


def patch_content(patch: PatchedFile, content: str) -> str:
    lines: List[Optional[str]] = [l + '\n' for l in content.splitlines()]

    for hunk in patch:
        for line in hunk.source_lines():
            if line.is_context:
                continue
            elif line.is_removed:
                lines[line.source_line_no-1] = None

    lines_removed = [l for l in lines if l is not None]

    for hunk in patch:
        for line in hunk.target_lines():
            if line.is_context:
                continue
            elif line.is_added:
                lines_removed.insert(line.target_line_no-1, line.value)
    return ''.join(lines_removed)


def patch_files(diff_text: str, target_dir, strip: int = 0):
    patches = PatchSet(diff_text)
    for patch in patches:
        *_, path = patch.path.split('/', strip)
        path = os.path.join(target_dir, path)

        with open(path) as f:
            content = f.read()
        patched_content = patch_content(patch, content)

        with open(path, mode='w') as f:
            f.write(patched_content)
