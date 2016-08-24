from .base_match import BaseMatchAdapter
from snownlp.sim import bm25

class ChnClosestMeaningAdapter(BaseMatchAdapter):
    """
    This adapter selects a response by comparing the tokenized form of the
    input statement's text, with the tokenized form of possible matching
    statements. For each possible match, the sum of the Cartesian product of
    the path similarity of each statement is compared. This process simulates
    an evaluation of the closeness of synonyms. The known statement with the
    greatest path similarity is then returned.
    """

    def __init__(self, **kwargs):
        super(ChnClosestMeaningAdapter, self).__init__(**kwargs)

    def get_similarity(self, string1, string2):
        """
        Calculate the similarity of two statements.
        This is based on the total similarity between
        each word in each sentence.
        """
        return bm25.BM25([string1]).simall(string2)[0]

    def get(self, input_statement):
        """
        Takes a statement string and a list of statement strings.
        Returns the closest matching statement from the list.
        """
        statement_list = self.context.storage.get_response_statements()

        if not statement_list:
            if self.has_storage_context:
                # Use a randomly picked statement
                self.logger.info(
                    u'No statements have known responses. ' +
                    u'Choosing a random response to return.'
                )
                return 0, self.context.storage.get_random()
            else:
                raise self.EmptyDatasetException()

        # Get the text of each statement
        text_of_all_statements = []
        for statement in statement_list:
            text_of_all_statements.append(statement.text)

        # Check if an exact match exists
        if input_statement.text in text_of_all_statements:
            return 1, input_statement

        closest_statement = None
        closest_similarity = -1
        total_similarity = 0

        # For each option in the list of options
        for statement in text_of_all_statements:
            similarity = self.get_similarity(input_statement.text, statement)

            total_similarity += similarity

            if similarity > closest_similarity:
                closest_similarity = similarity
                closest_statement = statement

        try:
            confidence = closest_similarity / total_similarity
        except:
            confidence = 0

        return confidence, next(
            (s for s in statement_list if s.text == closest_statement), None
        )
