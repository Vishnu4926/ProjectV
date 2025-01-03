import os

def clear_cache():
    print("Clearing memory cache...")
    os.system('sync; echo 3 > /proc/sys/vm/drop_caches')
    print("Memory cache cleared.")

if __name__ == "__main__":
    clear_cache()
