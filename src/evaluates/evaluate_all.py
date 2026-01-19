import argparse
import os
import subprocess

SOURCE_FOLDER = "src/evaluates/"

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    #     parser.add_argument("-s", "--save_dir", default = "result")
    parser.add_argument("-d", "--delimiter", default=" ")
    parser.add_argument("-e", "--method_dir", default="../data/models/Word2vec_Google/")
    args = parser.parse_args()

    for emb_name in os.listdir(args.method_dir):
        subprocess.run(
            [
                "python",
                "src/evaluates/evaluate_emb_folder.py",
                "-d",
                args.delimiter,
                "-e",
                os.path.join(args.method_dir, emb_name),
            ]
        )
