# TODO (stretch goal): validate chunks before hand-off to vectorization
#
# Planned checks:
# - no empty chunks (page_content is not blank)
# - every chunk has "title" and "source" in metadata (needed for provenance)
# - chunk size is within limit (<= chunk_size)
# - flag pages that produced zero chunks (possible cleaning issue)