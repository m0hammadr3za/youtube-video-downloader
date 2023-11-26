def readable_size(size):
    KB = 1024
    MB = KB * KB
    GB = MB * KB

    if size < MB:
        return f"{size/KB:.2f} KB"
    elif size < GB:
        return f"{size/MB:.2f} MB"
    else:
        return f"{size/GB:.2f} GB"