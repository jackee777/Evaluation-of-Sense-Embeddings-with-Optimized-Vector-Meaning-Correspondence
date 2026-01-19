import argparse
import os
import subprocess

SOURCE_FOLDER = "src/evaluates/"

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    #     parser.add_argument("-s", "--save_dir", default = "result")
    parser.add_argument("-d", "--delimiter", default=" ")
    parser.add_argument(
        "-e",
        "--embedding_path",
        default="../data/models/Word2vec_Google/GoogleNews-vectors-negative300.bin",
    )
    args = parser.parse_args()

    evaluations = [
        "evaluate_EmbByNeighbors.py",
    ]  # , "evaluate_EmbByWiC.py"] #"evaluate_EmbByAnalogy.py",
    evaluations = [
        os.path.join(SOURCE_FOLDER, evaluation) for evaluation in evaluations
    ]
    for evaluation in evaluations:
        subprocess.run(
            ["python", evaluation, "-d", args.delimiter, "-e", args.embedding_path]
        )
