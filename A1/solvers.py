class SentenceCorrector(object):
    def __init__(self, cost_fn, conf_matrix):
        self.conf_matrix = conf_matrix
        self.cost_fn = cost_fn
        self.orig_state = None
        self.word_range = []
        self.special_words = []

        # You should keep updating following variable with best string so far.
        self.best_state = None

    def possible_errors(self):
        error_corrector = {}
        for elem in self.conf_matrix:
            for val in self.conf_matrix[elem]:
                if val in error_corrector:
                    error_corrector[val].append(elem)
                else:
                    error_corrector[val] = [elem]
        return error_corrector

    # def correct_word(self, possible_errors, sentence, word, start_index):
    #     cost = self.cost_fn(sentence)
    #     ind_to_update = start_index
    #     new_char = ''
    #     for ind in range(len(word)):
    #         char = word[ind]
    #         if char in possible_errors:
    #             for changed_char in possible_errors[char]:
    #                 new_sentence = sentence[0:ind] + \
    #                     changed_char + sentence[ind+1:]
    #                 new_cost = self.cost_fn(new_sentence)
    #                 if new_cost < cost:
    #                     ind_to_update += ind+1
    #                     cost = new_cost
    #                     new_char = changed_char
    #     if ind_to_update != start_index:
    #         sentence = sentence[0:ind_to_update] + \
    #             new_char + sentence[ind_to_update+1:]
    #     else:
    #         ind_updated1 = start_index
    #         ind_updated2 = start_index
    #         new_char1 = ''
    #         new_char2 = ''
    #         for ind1 in range(len(word)):
    #             for ind2 in range(ind1 + 1, len(word)):
    #                 char1 = word[ind1]
    #                 char2 = word[ind2]
    #                 if (char1 in possible_errors) and (char2 in possible_errors):
    #                     for changed_char1 in possible_errors[char1]:
    #                         for changed_char2 in possible_errors[char2]:
    #                             new_sentence = sentence[0:ind1] + \
    #                                 changed_char1 + \
    #                                 sentence[ind1+1:ind2] + \
    #                                 changed_char2 + sentence[ind2 + 1:]
    #                             new_cost = self.cost_fn(new_sentence)
    #                             if new_cost < cost:
    #                                 ind_updated1 += ind1 + 1
    #                                 ind_updated2 += ind2 + 1
    #                                 cost = new_cost
    #                                 new_char1 = changed_char1
    #                                 new_char2 = changed_char2
    #         if ind_updated1 != start_index and ind_updated2 != start_index:
    #             sentence = sentence[0:ind_updated1] + \
    #                 new_char1 + \
    #                 sentence[ind_updated1+1:ind_updated2] + \
    #                 new_char2 + sentence[ind_updated2 + 1:]
    #     self.best_state = sentence

    def charToWord(self, char_index):
        num = 0
        for [s, f] in self.word_range:
            if s <= char_index and f > char_index:
                return num
            else:
                num += 1

    def to_explore_for_2_updates(self, sentence, start, end, possible_errors):
        to_explore_for_2_updates = False
        cost = self.cost_fn(sentence[start:end])
        for ind in range(start, end):
            char = sentence[ind]
            if char in possible_errors:
                for changed_char in possible_errors[char]:
                    new_word = sentence[start:ind] + \
                        changed_char + sentence[ind+1:end]
                    new_cost = self.cost_fn(new_word)
                    if new_cost <= cost:
                        to_explore_for_2_updates = True
                        break
                if (to_explore_for_2_updates):
                    break
        return to_explore_for_2_updates

    def update_single(self, sentence, possible_errors, ind_updated, toProceed, words_updated):
        cost = self.cost_fn(sentence)
        ind_to_update = -1
        new_char = ''
        num_word = 0
        for ind in range(len(sentence)):
            if sentence[ind] == " ":
                num_word += 1
            if ind_updated[ind] == 1:
                continue
            char = sentence[ind]
            if char in possible_errors:
                for changed_char in possible_errors[char]:
                    new_sentence = sentence[0:ind] + \
                        changed_char + sentence[ind+1:]
                    new_cost = self.cost_fn(new_sentence)
                    if new_cost < cost:
                        self.special_words[num_word] += 1
                        ind_to_update = ind
                        cost = new_cost
                        new_char = changed_char
        if ind_to_update != -1:
            ind_updated[ind_to_update] = 1
            word_ind = self.charToWord(ind_to_update)
            words_updated[word_ind] += 1
            sentence = sentence[0:ind_to_update] + \
                new_char + sentence[ind_to_update+1:]
            toProceed = True
        else:
            toProceed = False
        return sentence, toProceed

    def update_double(self, sentence, possible_errors, toProceed, words_update_at_double, start, end):
        cost = self.cost_fn(sentence)
        ind_updated1 = -1
        ind_updated2 = -1
        new_char1 = ''
        new_char2 = ''
        word_num = 0
        to_explore_for_3_updates = [False]*len(self.word_range)
        for ind1 in range(start, end):
            if (sentence[ind1] == " " or sentence[ind1] == "\n"):
                word_num += 1
                continue
            if words_update_at_double[word_num] == 1:
                continue
            # elif (words_updated[word_num] == 1 or (not self.to_explore_for_2_updates(sentence, self.word_range[word_num][0], self.word_range[word_num][1], possible_errors))):
            if self.word_range[word_num][1] > ind1:
                end = self.word_range[word_num][1]
                start = self.word_range[word_num][0]
            if ((not self.to_explore_for_2_updates(sentence, start, end, possible_errors))):
                continue
            for ind2 in range(ind1 + 1, end):
                char1 = sentence[ind1]
                char2 = sentence[ind2]
                if (char1 in possible_errors) and (char2 in possible_errors):
                    for changed_char1 in possible_errors[char1]:
                        for changed_char2 in possible_errors[char2]:
                            new_sentence = sentence[0:ind1] + \
                                changed_char1 + \
                                sentence[ind1+1:ind2] + \
                                changed_char2 + sentence[ind2 + 1:]
                            new_cost = self.cost_fn(new_sentence)
                            if new_cost < cost:
                                ind_updated1 = ind1
                                ind_updated2 = ind2
                                cost = new_cost
                                new_char1 = changed_char1
                                new_char2 = changed_char2
                                to_explore_for_3_updates[word_num] = True
                            elif new_cost == cost:
                                to_explore_for_3_updates[word_num] = True
        if ind_updated1 != -1 and ind_updated2 != -1:
            word_ind = self.charToWord(ind_updated1)
            words_update_at_double[word_ind] = 1
            sentence = sentence[0:ind_updated1] + \
                new_char1 + \
                sentence[ind_updated1+1:ind_updated2] + \
                new_char2 + sentence[ind_updated2 + 1:]
            toProceed = True
        else:
            toProceed = False
        return sentence, toProceed, to_explore_for_3_updates

    def local_search(self, sentence, possible_errors):
        count = 0
        words_updated = [0]*len(self.word_range)
        words_update_at_double = [0] * len(self.word_range)

        ind_updated = [0]*len(sentence)
        toProceed = True
        while toProceed:
            sentence, toProceed = self.update_single(
                sentence, possible_errors, ind_updated, toProceed, words_updated)
            self.best_state = sentence

        # print("---------------------------")
        # for ind in range(len(self.special_words)):
        #     if self.special_words[ind] > 1:
        #         s, f = self.word_range[ind]
        #         print(self.orig_state[s:f]," ")
        # print("---------------------------")

        state_after_1_update = self.best_state

        toProceed = True
        for i in range(len(words_updated)):
            # check for SPECIAL words that were singly updated but the parent has some changes other than the current change that reduces the cost to some extent
            if words_updated[i] > 1:
                # or (words_updated[i] == 1 and self.orig_state[s:f]  # has more options to explore (can be found from update single )
                #                             )
                [s, f] = self.word_range[i]
                sentence = sentence[0: s] + self.orig_state[s:f] + sentence[f:]
        while (toProceed):
            sentence, toProceed, to_explore_for_3 = self.update_double(
                sentence, possible_errors, toProceed, words_update_at_double, 0, len(sentence))
            self.best_state = sentence

        words_update_at_double = [0] * len(self.word_range)
        for word_ind in range(len(self.special_words)):
            if self.special_words[word_ind] > 1 and words_updated[word_ind] == 1:
                # print(self.orig_state[self.word_range[word_ind]
                #       [0]: self.word_range[word_ind][1]])
                s, f = self.word_range[word_ind]
                old_sentence = sentence[0:s] + \
                    self.orig_state[s:f] + sentence[f:]
                new_sentence, toProceed, to_explore_for_3 = self.update_double(
                    old_sentence, possible_errors, toProceed, words_update_at_double, s, f)
                old_sentence = sentence[0: s] + \
                    state_after_1_update[s:f] + sentence[f:]
                # print(new_sentence)
                if (self.cost_fn(new_sentence) < self.cost_fn(old_sentence)):
                    sentence = new_sentence
                else:
                    sentence = old_sentence
        self.best_state = sentence

    def search(self, start_state):
        """
        :param start_state: str Input string with spelling errors
        """
        # You should keep updating self.best_state with best string so far.
        # self.best_state = start_state

        # Creating a list of 3 words in the sentence
        # j = 0
        # for i in range(len(start_state)):
        #     if start_state[i] == ' ':
        #         if j == 2:
        #             start_state = start_state[0:i] + ',' + start_state[i+1:]
        #             j = 0
        #         else:
        #             j += 1

        # trigrams = start_state.split(',')
        possible_errors = self.possible_errors()
        self.orig_state = start_state

        # Iterating over the trigrams
        # temp_state = ""
        # for trigram in trigrams:
        #     trigram = self.update_single(trigram, possible_errors)
        #     temp_state += trigram + ' '
        # self.best_state = temp_state[:-1]

        prev = 0
        for i in range(len(start_state)):
            if start_state[i] == " " or start_state[i] == "\n":
                self.word_range.append([prev, i])
                prev = i+1
        if prev < len(start_state):
            self.word_range.append([prev, len(start_state)])

        self.special_words = [0] * len(self.word_range)

        self.local_search(start_state, possible_errors)
        # self.best_state = start_state
        # start_ind = -1
        # word = ''
        # for i in range(len(start_state)):
        #     if (start_state[i] != " " and start_state[i] != "\n"):
        #         word += start_state[i]
        #     else:
        #         self.correct_word(possible_errors, self.best_state, word, start_ind)
        #         start_ind = i
        #         word = ''

        # raise Exception("Not Implemented.")
