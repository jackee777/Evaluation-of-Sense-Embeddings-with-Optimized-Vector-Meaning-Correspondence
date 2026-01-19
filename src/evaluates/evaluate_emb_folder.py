import argparse
import os
import subprocess

SOURCE_FOLDER = "src/evaluates/"

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    #     parser.add_argument("-s", "--save_dir", default = "result")
    parser.add_argument("-d", "--delimiter", default=" ")
    parser.add_argument(
        "-e", "--embedding_dir", default="../data/models/Word2vec_Google/"
    )
    args = parser.parse_args()

    for emb_name in os.listdir(args.embedding_dir):
        if emb_name[-4:] not in [".txt", ".bin"]:
            continue
        evaluations = [
            "evaluate_EmbByNeighbors.py",
        ]  # , "evaluate_EmbByWiC.py"] #"evaluate_EmbByAnalogy.py",
        evaluations = [
            os.path.join(SOURCE_FOLDER, evaluation) for evaluation in evaluations
        ]
        for evaluation in evaluations:
            subprocess.run(
                [
                    "python",
                    evaluation,
                    "-d",
                    args.delimiter,
                    "-e",
                    os.path.join(args.embedding_dir, emb_name),
                ]
            )
