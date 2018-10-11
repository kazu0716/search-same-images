from PIL import Image
import imagehash
import glob

if __name__ == '__main__':
    print(glob.glob('images/*.png', recursive=True))
