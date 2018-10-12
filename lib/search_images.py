# -*- using:utf-8 -*-
import time
import sys
from PIL import Image
import imagehash
import pickle
from tinydb import Query, TinyDB

class SearchImages(object):
 
 def __init__(self):
    db = TinyDB("./db.json")
    self.table = db.table("image-hash", cache_size=10000)
    self.query = Query()

 def __insert_db(self,data):
    try:
        self.table.insert(self,data)
    except Exception as e:
        print(e)


 def __gen_image_hash(self,path, alg):
    if alg == "whash":
        return imagehash.whash(Image.open(path))
    elif alg == "phash":
        return imagehash.phash(Image.open(path))
    elif alg == "dhash":
        return imagehash.dhash(Image.open(path))
    elif alg == "ahash":
        return imagehash.average_hash(Image.open(path))
    else:
        sys.exit(1)


 def upload_images(self,image_file):
    if len(self.table.search(query.full_path == image_file)) == 0:
        p_hash = self.__gen_image_hash(image_file, "phash")
        w_hash = self.__gen_image_hash(image_file, "whash")
        data = {
            "file_name": image_file.split("/")[-1],
            "full_path": image_file,
            "p_hash": str(p_hash),
            "p_row_hash": repr(pickle.dumps(p_hash)),
            "w_hash": str(w_hash),
            "w_row_hash": repr(pickle.dumps(w_hash))
        }
        self.__insert_db(data)


 def search_images(image_file):
    all_data = self.__table.all()

    p_hash = self.__gen_image_hash(image_file, "phash")
    w_hash = self.__gen_image_hash(image_file, "whash")

    check_hash_string = self.table.search(
        (self.query.p_hash == str(p_hash)) | (self.query.w_hash == str(w_hash))
    )
    if len(check_hash_string) == 0:
        result["exact_matches"].append({
            "match_file": {
                "searched_file": image_file.split("/")[-1]
                # "hit_file": data["file_name"]
            },
            "image_hash": check_hash_string
        })
    else:
        for data in all_data:
            diff_p_hash = pickle.loads(eval(data["p_row_hash"])) - p_hash
            diff_w_hash = pickle.loads(eval(data["w_row_hash"])) - w_hash
            if diff_p_hash < 10 or diff_w_hash < 10:
                result["partial_matches"].append({
                    "match_file": {
                        "searched_file": image_file.split("/")[-1],
                        "hit_file": data["file_name"]
                    },
                    "p_hash": {
                        "diff": diff_p_hash
                    },
                    "w_hash": {
                        "diff": diff_w_hash
                    }
                })
    return result