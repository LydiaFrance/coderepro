import os
from test_bert import Classifier, TextClassificationDataset
import test_bert
from terminaltables import SingleTable
from textwrap import wrap

test_data_path = "./data/"

categories = ["General checks", "Code quality", "Documentation", "Testing", "Summary"]

#let's do category, text, score for now
feedback_table = [["Category", "Feedback", "Score"]]

for idx, cat in enumerate(categories): 
    with open(os.path.join(test_data_path, f"response_{idx+1}.txt")) as fin:
        raw_text = fin.read()
        eval_text = raw_text.replace('\n', '').replace("*", " ")
        sentiment_score = test_bert.evaluate_bert(eval_text)
        cat_feedback = []
        cat_feedback.append(cat)
        cat_feedback.append(raw_text)
        cat_feedback.append("{:.2f}%".format(sentiment_score))
        feedback_table.append(cat_feedback)

#print table
table_instance = SingleTable(feedback_table, "Feedback")

max_width = table_instance.column_max_width(1)
for entry in table_instance.table_data:
    wrapped_string = "\n".join(wrap(entry[1], max_width))
    entry[1] = wrapped_string

print(table_instance.table)