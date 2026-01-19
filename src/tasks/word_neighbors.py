import os

import gensim
import networkx as nx
import numpy as np
import pandas as pd
from tqdm import tqdm


def get_word_data(word, data, max_dis=2, rm_words=["nan", "none", "NaN", "None"]):
    data = data.astype(str)
    dis_to_column = {
        0: ["synonyms"],
        1: ["hypernyms-1", "hyponyms-1"],
        2: ["siblings", "hypernyms-2", "hyponyms-2"],
    }
    #     print(column)

    word_data = [[set() for i in range(max_dis + 1)] for j in range(len(data.values))]
    for dis in range(max_dis + 1):
        for column in dis_to_column[dis]:
            for j, corrects in enumerate(data[column].values):
                correct_words = set(corrects.split()) - set(rm_words)
                word_data[j][dis] |= correct_words
    return word_data


def get_data(target_path, words, include_babelnet=True):
    dataset = {}
    for word in words:
        rm_words = [word, "nan", "none", "NaN", "None"]
        if f"{word}.csv" not in os.listdir(target_path):
            print(f"{word}.csv doesn`t exist in {target_path}")
            continue
        word_df = pd.read_csv(os.path.join(target_path, f"{word}.csv"))
        if not include_babelnet:
            word_df = word_df.query('synsets.str.contains("wn")')
        #             print(word_df.head())
        dataset[word] = get_word_data(word, word_df, max_dis=2, rm_words=rm_words)
    return dataset


def evaluate_word_neighbors(
    word_neighbors,
    word_vector,
    data,
    use_words,
    tag_dict,
    topns,
    delimiter=" ",
    debug_word="",
):  # when nodebug, debug_word = ""
    max_dis = 2
    answer_words = set(tag_dict.keys())

    sense_score = {t: [] for t in topns}
    vector_score = {t: [] for t in topns}
    maxmatch_score = {t: [] for t in topns}
    vdetail_info = {t: [] for t in topns}
    mdetail_info = {t: [] for t in topns}

    costs = []
    dataset_sense_nums = []
    sense_nums = []
    for word in tqdm(sorted(list(data.keys()))):
        if debug_word != "":
            if word != debug_word:
                continue
        if word not in word_neighbors:
            continue

        word_score = {t: [] for t in topns}
        sense_nums.append(len(tag_dict[word]))
        dataset_sense_nums.append(len(data[word]))
        t_matrix = {
            t: np.zeros(
                (
                    len(tag_dict[word]) + len(data[word]),
                    len(tag_dict[word]) + len(data[word]),
                )
            )
            for t in topns
        }
        m = -1
        for tag in tag_dict[word]:
            m += 1
            if debug_word != "":
                print(word + tag)
            max_score = {t: 0 for t in topns}
            info = {t: [word, len(data[word])] for t in topns}
            detail_max_score = {t: [0 for i in range(max_dis + 1)] for t in topns}
            detail_upper_bound = {t: 0 for t in topns}

            candidates = [
                word.split(delimiter)[0] for word in word_neighbors[word + tag]
            ]
            for n, corr in enumerate(data[word]):
                answer = set()
                for i in range(max_dis + 1):
                    answer |= corr[i]

                for t in topns:
                    if debug_word != "":
                        if t != 5:
                            continue
                    cand = candidates[:t]
                    if debug_word != "":
                        print("cand", " ".join(list(cand)))
                    #                         print("answer", " ".join(list(answer)))
                    cand = set(cand) - {word}
                    AP = len(cand & answer)
                    if debug_word != "":
                        print("cand & answer", cand & answer)
                    #                     print(matrix)
                    t_matrix[t][m][len(tag_dict[word]) + n] = AP
                    t_matrix[t][len(tag_dict[word]) + n][m] = AP
                    if AP / t >= max_score[t]:
                        max_score[t] = AP / t
                    for i in range(max_dis + 1):
                        detail_answer = corr[i]
                        for j in range(i):
                            detail_answer -= corr[j]
                        if AP / t >= max_score[t]:
                            detail_max_score[t][i] = len(cand & detail_answer)

            for n, corr in enumerate(data[word]):
                answer = set()
                for i in range(max_dis + 1):
                    answer |= corr[i]
                for t in topns:
                    upper_bound = len(answer_words & answer)
                    upper_bound = min([upper_bound, t])
                    detail_upper_bound[t] = max([detail_upper_bound[t], upper_bound])

            for t in topns:
                word_score[t].append(max_score[t])

            for t in topns:
                info[t].append(len(tag_dict[word]))
                info[t].extend(detail_max_score[t])
                info[t].append(detail_upper_bound[t])
                vdetail_info[t].append(info[t])

        if len(tag_dict[word]) != 0:
            for t in topns:
                # sense_matching
                sense_sco = np.sum(
                    [
                        np.max(t_matrix[t][i])
                        for i in range(
                            len(tag_dict[word]), len(tag_dict[word]) + len(data[word])
                        )
                    ]
                ) / max([len(tag_dict[word]), len(data[word])])
                sense_score[t].append(sense_sco / t)

                # vector score
                vector_score[t].append(
                    np.sum(word_score[t]) / max([len(tag_dict[word]), len(data[word])])
                )

                # max_matching
                g1 = np.arange(len(tag_dict[word]))
                g2 = np.arange(
                    len(tag_dict[word]), len(tag_dict[word]) + len(data[word])
                )
                G = nx.Graph(t_matrix[t])
                d = nx.max_weight_matching(G)
                matching_score = np.sum([t_matrix[t][i][j] for i, j in d])
                maxmatch_score[t].append(
                    matching_score / max([len(tag_dict[word]), len(data[word])]) / t
                )

                set_d = set(
                    [
                        (i, j - len(tag_dict[word]))
                        if j > i
                        else (j, i - len(tag_dict[word]))
                        for i, j in d
                    ]
                )

                mupper_bound = []
                for n, corr in enumerate(data[word]):
                    answer = set()
                    for i in range(max_dis + 1):
                        answer |= corr[i]
                    upper_bound = len(answer_words & answer)
                    upper_bound = min([upper_bound, t])
                    mupper_bound.append(upper_bound)
                mupper_bound = sorted(mupper_bound, reverse=True)
                mdetail_upper_bound = np.mean(
                    mupper_bound[: min([len(tag_dict[word]), len(data[word])])]
                )

                if len(set_d) == 0:
                    mdetail_info[t].append(
                        [
                            word,
                            len(data[word]),
                            len(tag_dict[word]),
                            0,
                            0,
                            0,
                            mdetail_upper_bound,
                        ]
                    )

                m = -1
                for tag in tag_dict[word]:
                    minfo = [word, len(data[word]), len(tag_dict[word])]
                    mdetail_max_score = [0 for i in range(max_dis + 1)]
                    m += 1
                    candidates = [
                        word.split(delimiter)[0] for word in word_neighbors[word + tag]
                    ]
                    for n, corr in enumerate(data[word]):
                        answer = set()
                        for i in range(max_dis + 1):
                            answer |= corr[i]
                        if (m, n) not in set_d:
                            continue
                        cand = candidates[:t]
                        cand = set(cand) - {word}
                        for i in range(max_dis + 1):
                            detail_answer = corr[i]
                            for j in range(i):
                                detail_answer -= corr[j]
                            mdetail_max_score[i] += len(cand & detail_answer)
                        minfo.extend(mdetail_max_score)
                        minfo.append(mdetail_upper_bound)
                        mdetail_info[t].append(minfo)

    print("precision @{}".format(topns))
    #     print("the number of words", len(score))
    print("average of number of words", np.mean(sense_nums))
    #     print("evaluation score", np.mean(score))
    #     [print(score[t]) for t in topns]
    return [
        [
            t,
            len(word_vector.index_to_key),
            len(vector_score[t]),
            np.mean(sense_nums),
            np.mean(dataset_sense_nums),
            np.mean(sense_score[t]),
            np.mean(vector_score[t]),
            np.mean(maxmatch_score[t]),
            pd.DataFrame(
                np.asarray([sense_score[t], vector_score[t], maxmatch_score[t]]).T,
                columns=["sense_score", "vector_score", "maxmatch_score"],
            ),
            pd.DataFrame(
                vdetail_info[t],
                columns=[
                    "word",
                    "len_dataset",
                    "len_size",
                    "depth-0",
                    "depth-1",
                    "depth-2",
                    "upper",
                ],
            ),
            pd.DataFrame(
                mdetail_info[t],
                columns=[
                    "word",
                    "len_dataset",
                    "len_size",
                    "depth-0",
                    "depth-1",
                    "depth-2",
                    "upper",
                ],
            ),
        ]
        for t in topns
    ]
