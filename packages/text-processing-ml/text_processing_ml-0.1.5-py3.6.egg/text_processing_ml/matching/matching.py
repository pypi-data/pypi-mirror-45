import itertools
import jellyfish

class MatchText:
    def __init__(self):
        pass

    def generate_list_combinations_unordered(self, first: list, second: list):
        iterator = map(''.join,
                       itertools.chain(
                           itertools.product(first, second),
                           itertools.product(second, first)
                       ))
        return list(iterator)

    def generate_list_combinations_ordered(self, first: list, second: list):
        iterator = map(''.join, itertools.product(first, second))
        return list(iterator)

    def combine_lists(self, lists, ordered=True):
        if ordered:
            generate_list_combinations = self.generate_list_combinations_ordered
        else:
            generate_list_combinations = self.generate_list_combinations_unordered
        final_list = lists[0]
        num_lists = len(lists)
        for start_index in range(1, num_list-1):
            for index in range(1, num_lists):
                final_list += generate_list_combinations(
                    final_list,
                    lists[index]
                )
        return list(set(final_list))

    def filter_by_length(self, substrings: list, substring_len: int) -> list:
        """
        Filter the substrings by their length
        
        Paramters
        ---------
        substrings - a list of substrings of various lengths
        substring_len - the filter criteria of the function
        return substrings only matching this length
        if substring_len == -1 return all substrings
        
        Output
        ------
        return the filtered list of substrings
        """
        if substring_len == -1:
            return substrings
        else:
            new_substrings = []
            for substring in substrings:
                if len(substring) == substring_len:
                    new_substrings.append(substring)
            return new_substrings
        
    def match_lists(self, lists: list, text: str, substring_len: int, ordered: bool=True):
        """
        search a piece of text for all possible
        combinations of all tokens of a set of lists.
        Assumes tokens appear contigiously.

        Parameters
        ----------
        lists - a list of lists containing different tokens

        text - the text to seach over

        substring_len - the desired length of the substring
        if substring_len == -1 then return substrings of any length

        ordered [optional] - whether or not the tokens appear in 
        the order passed in, ordered assumes they do,
        unordered tries every possible combination.
        
        Output
        ------
        Returns all matching substrings
        """
        substrings = combine_lists(lists, ordered=ordered)
        text = "".join(text)
        found_substrings = []
        for substring in substrings:
            if substring in text:
                found_substrings.append(substring)
        found_substrings = self.filter_by_length(
            found_substrings, substring_len
        )
        return found_substrings

    def fuzzy_match(self, substring, text, ordered: bool=True, tolerance: int=1):
        """
        Perform a fuzzy match based on edit distance.
        if ordered use levenshtein distance,
        if unordered use damerau levenshtein distance.

        Parameters
        ----------
        substring - the substring to match against

        text - the text to seach over
        
        ordered [optional] - whether or not the tokens appear in 
        the order passed in, ordered assumes they do,
        unordered tries every possible combination.

        tolerance - the maximum edit distance to consider
        
        Output
        ------
        returns best fuzzy match to the substring
        """

        if ordered:
            distance_metric = jellyfish.levenshtein_distance
        else:
            distance_metric = jellyfish.damerau_levenshtein_distance

        possible_matches = []
        for end_index in range(len(substring), len(text), len(substring)):
            start_index = end_index - len(substring)
            distance = distance_metric(substring, text[start_index:end_index])
            if distance <= tolerance:
                possible_matches.append((substring, distance))
        best_match_distance = tolerance+1
        best_match = ''
        for match in possible_matches:
            if match[1] < best_match_distance:
                best_match = match[0]
                best_match_distance = match[1]
        return best_match
                
    def fuzzy_match_lists(self, lists: list, text: str, substring_len: int, ordered: bool=True, tolerance: int=1):
        """
        search a piece of text for all possible fuzzy
        combinations of all tokens of a set of lists.
        Assumes tokens appear contigiously.

        Parameters
        ----------
        lists - a list of lists containing different tokens
        
        text - the text to seach over

        substring_len - the desired length of the substring
        if substring_len == -1 then return substrings of any length
        
        ordered [optional] - whether or not the tokens appear in 
        the order passed in, ordered assumes they do,
        unordered tries every possible combination.

        tolerance - the maximum edit distance to consider
        Output
        ------
        Returns all fuzzy matching substrings
        """
        substrings = combine_lists(lists, ordered=ordered)
        text = "".join(text)
        fuzzy_matches = []
        for substring in substrings:
            match = fuzzy_match(substring, text,
                                ordered=ordered,
                                tolerance=tolerance)
            fuzzy_matches.append(match)
        fuzzy_matches = self.filter_by_length(
            fuzzy_matches, substring_len
        )
        return fuzzy_matches
