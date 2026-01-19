import argparse
import os
import pickle
import warnings

import gensim
import numpy as np
import pandas as pd
from tasks.word_neighbors import evaluate_word_neighbors, get_data
from utils import *

warnings.filterwarnings("ignore", category=DeprecationWarning)

import yaml

# TODO: limited PoS, delimiter, tag list, MSD-1030

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    #     parser.add_argument("-s", "--save_dir", default = "result")
    #     parser.add_argument("-t", "--tasks",
    #                         default = " ".join(["WordSim", "SimLex", "MEN", "SimVerb", "SCWS", "MultiSimLex", "RareWord", "Card"]))
    parser.add_argument("-d", "--delimiter", default=" ")
    parser.add_argument(
        "-e",
        "--embedding_path",
        default="../data/models/Word2vec_Google/GoogleNews-vectors-negative300.bin",
    )
    args = parser.parse_args()

    #     save_dir = args.save_dir
    #     tasks = args.tasks.split()
    if args.delimiter in {"POS", "SYNSET", "SENSE"}:
        delimiter = f"-{args.delimiter}-"
    else:
        delimiter = args.delimiter
    embedding_name = args.embedding_path
    metric = "WORD_NEIGHBORS"

    with open("config/config.yml") as file:
        config = yaml.safe_load(file.read())
    save_dir = config["save_dir"]
    checkout_dir = config["checkout_dir"]
    embedding_check_path = "embeddings"
    neighbors_check_path = "neighbors"
    dataset_path = "dataset/Word_Neighbors"
    topns = [1, 5, 10]
    tasks = config["neighbors_tasks"]

    # when nodebug, debug_word = ""
    debug_word = ""

    if os.path.basename(embedding_name)[:6] == "vector":
        compact_embedding_name = os.path.join(
            embedding_name.split("/")[-2], os.path.basename(embedding_name)
        ).replace("/", "_")
    else:
        compact_embedding_name = os.path.basename(embedding_name)
    save_path = os.path.join(save_dir, compact_embedding_name, metric)
    os.makedirs(save_path, exist_ok=True)

    try:
        word_vector = gensim.models.KeyedVectors.load_word2vec_format(
            embedding_name, binary=False
        )
    except:
        try:
            word_vector = gensim.models.KeyedVectors.load_word2vec_format(
                embedding_name, binary=True
            )
        except:
            word_vector = gensim.models.Word2Vec.load(embedding_name)
            word_vector = word_vector.wv

    if "neighbors_use_vocabs" in config:
        use_vocabs = set(pickle.load(open(config["neighbors_use_vocabs"], "rb")))
        check_path = os.path.join(
            checkout_dir,
            embedding_check_path,
            os.path.basename(config["neighbors_use_vocabs"]),
        )
        os.makedirs(check_path, exist_ok=True)

        if compact_embedding_name not in os.listdir(check_path):
            index_to_key = [
                word
                for word in word_vector.index_to_key
                if word.split(delimiter)[0] in use_vocabs
            ]

            with open(
                os.path.join(check_path, compact_embedding_name + ".txt"), "w"
            ) as f:
                f.write(
                    "{} {}\n".format(len(index_to_key), word_vector.vectors.shape[1])
                )
                for word in index_to_key:
                    f.write(
                        "{} {}\n".format(
                            word, " ".join(list(map(str, word_vector[word])))
                        )
                    )

        word_vector = gensim.models.KeyedVectors.load_word2vec_format(
            os.path.join(check_path, compact_embedding_name + ".txt"), binary=False
        )
    else:
        use_vocabs = None

    if "neighbors_use_words" in config:
        use_words = set(pickle.load(open(config["neighbors_use_words"], "rb")))
    else:
        use_words = set()
        for task in tasks:
            use_words |= set(os.listdir(os.path.join(dataset_path, task)))
        use_words = [word.replace(".csv", "") for word in use_words]

    tag_dict = dict()
    # limited_pos
    for key in word_vector.index_to_key:
        if delimiter not in key:
            word = key
            tag = ""
        else:
            word, tag = key.split(delimiter)
            tag = delimiter + tag
        if word not in tag_dict:
            tag_dict[word] = [tag]
        else:
            tag_dict[word].append(tag)

    os.makedirs(os.path.join(checkout_dir, neighbors_check_path), exist_ok=True)
    if "neighbors_use_vocabs" in config:
        vocab_path = os.path.basename(config["neighbors_use_vocabs"])
    else:
        vocab_path = "None"
    check_path = os.path.join(checkout_dir, neighbors_check_path, vocab_path)
    os.makedirs(check_path, exist_ok=True)
    if compact_embedding_name not in os.listdir(check_path):
        with open(os.path.join(check_path, compact_embedding_name), "w") as f:
            for word in use_words:
                if word not in tag_dict:
                    continue
                for tag in tag_dict[word]:
                    similar_words = [
                        info[0]
                        for info in word_vector.most_similar(
                            word + tag, topn=np.max(topns)
                        )
                    ]
                    f.write("{} {}\n".format(word + tag, " ".join(similar_words)))
    with open(os.path.join(check_path, compact_embedding_name), "r") as f:
        word_neighbors = {}
        for line in f:
            info = line.split()
            word, similar_words = info[0], info[1:]
            word_neighbors[word] = similar_words

    for task in tasks:
        print(task)
        if task not in os.listdir(save_path):
            os.mkdir(os.path.join(save_path, task))
        if "detail" not in os.listdir(os.path.join(save_path, task)):
            os.mkdir(os.path.join(save_path, task, "detail"))
        data = get_data(
            os.path.join(dataset_path, task), words=use_words, include_babelnet=True
        )
        evaluation_results = []
        P_scores = evaluate_word_neighbors(
            word_neighbors,
            word_vector,
            data,
            use_words,
            tag_dict,
            topns=topns,
            delimiter=delimiter,
            debug_word=debug_word,
        )

        for score in P_scores:
            info = [task]
            info.extend(["Prec_emb", None])
            info.extend(score[:-3])
            if debug_word == "":
                score[-3].to_csv(
                    os.path.join(
                        save_path, task, "detail", "result_all_" + str(info[3])
                    )
                )
                score[-2].to_csv(
                    os.path.join(
                        save_path, task, "detail", "normal_Prec_emb_" + str(info[3])
                    )
                )
                score[-1].to_csv(
                    os.path.join(
                        save_path, task, "detail", "max_Prec_emb_" + str(info[3])
                    )
                )
            evaluation_results.append(info)
            print(info)

        if debug_word == "":
            df = pd.DataFrame(
                evaluation_results,
                columns=[
                    "pattern",
                    "evaluate_method",
                    "Negative Sampling",
                    "topn",
                    "vocab size",
                    "number of words",
                    "number of sense (ave)",
                    "number of dataset sense (ave)",
                    "evaluation score(no cost)",
                    "evaluation sense score(no cost)",
                    "evaluation max score(no cost)",
                ],
            )
            df.to_csv(os.path.join(save_path, task, "all"), index=False)
