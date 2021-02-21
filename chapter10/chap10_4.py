"""
@BY: Yang LIU
@DATE: 17-11-2020
"""


def hidden_path_probability(path, d, transition_dic):
    probability = 1/2
    for i in range(len(path)-2+1):
        state_transition = path[i:i+d]
        probability *= transition_dic[state_transition]
    return probability


def outcome_probability_based_on_hiddenpath(path, outcome, outcome_dic):
    probability = 1
    for i in range(len(path)):
        probability *= outcome_dic[(path[i], outcome[i])]
    return probability


if __name__ == "__main__":   

    # path = "AAAABBAAABBBAABAABBBBBABBBAAABAAAAABBABBBBABAAAABB"
    # d = 2
    # transition_dic = {"AA": 0.606, "AB": 0.394, "BA": 0.3, "BB": 0.7}
    # print(hidden_path_probability(path, d, transition_dic))

    path = "BBAAAABBABBBABBAABBAABBABABBBBABAAAAABAABBAABAAAAB"
    outcome = "xyyxyzyyyyyxyxzzxxzxyyxyyzxyxzyyxzxyxyzxxyzzyyzxyy"
    outcome_dic = {("A", "x"): 0.123, ("A", "y"): 0.52, ("A", "z"): 0.357, ("B", "x"): 0.276, ("B", "y"): 0.6, ("B", "z"): 0.124}
    print(outcome_probability_based_on_hiddenpath(path, outcome, outcome_dic))