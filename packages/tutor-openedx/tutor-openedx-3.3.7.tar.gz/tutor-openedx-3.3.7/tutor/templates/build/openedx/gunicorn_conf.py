import multiprocessing

# The recommended number of workers is twice the
# CPU count plus one
workers = (multiprocessing.cpu_count() * 2) + 1
