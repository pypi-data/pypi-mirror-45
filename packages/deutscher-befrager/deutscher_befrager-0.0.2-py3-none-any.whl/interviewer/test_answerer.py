import unittest
import pprint
from answerer import next_question

pp = pprint.PrettyPrinter(indent=4)


class TestNextQuestion(unittest.TestCase):
    def test_number_of_answers(self):
        """ Test that questions without answers come first """
        questions = dict()
        inital_time = 1556434717
        for x in range(10):
            scaler = x + 1
            answer = f"Answer {scaler}"
            answers = [answer] * scaler
            record = {'Q': f"Question {scaler}", 'A': answers}
            timestamp = inital_time + x
            questions[timestamp] = record

        q_keys = sorted(list(questions.keys()))
        first_key = q_keys[0]
        last_key = q_keys[len(q_keys) - 1]

        final_keys = []
        test_cycles = 1000
        for x in range(test_cycles):
            final_keys.append(next_question(questions))
        # pp.pprint(first_question)
        # pp.pprint(final_keys)
        first_key_count = len(list(filter(lambda k: k == first_key, final_keys)))
        last_key_count = len(list(filter(lambda k: k == last_key, final_keys)))

        first_key_rate = first_key_count / test_cycles
        last_key_rate = last_key_count / test_cycles
        assert first_key_rate > 0.15 and first_key_rate < 0.4, "questions with few answers get answered first"
        assert last_key_rate < 0.05, "questions with lots of answers get answered rarly"


if __name__ == '__main__':
    unittest.main()


