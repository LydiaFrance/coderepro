import os
from pathlib import Path
from test_bert import Classifier, TextClassificationDataset
import test_bert
from terminaltables import SingleTable
from textwrap import wrap
import json

CWD = Path(__file__).resolve().parent

test_data_path = CWD.parents[1].resolve() / "temp_repo/output/"

categories = ["Code Quality", "Documentation", "Testing", "Notebooks"]
file_suffixes = ["codequality", "documentation", "testing", "notebooks"]

#let's do category, text, score for now
feedback_table = [["Category", "Feedback", "Score"]]

#first summarize the manual checks without the LLM
fc_table_entry = ["File checks"]
fc_table_entry_text = ""
with open( test_data_path / "feedback.json") as f:
    file_check_dict = json.load(f)
for fc_item in file_check_dict.values():
    fc_table_entry_text += fc_item
    fc_table_entry_text += '\n'
fc_table_entry.append(fc_table_entry_text)
fc_table_entry.append("No Score")

feedback_table.append(fc_table_entry)

#and now to BERT
sum_of_scores = 0
for idx, cat in enumerate(categories): 
    with open(os.path.join(test_data_path, f"response_{file_suffixes[idx]}_1.txt")) as fin:
        raw_text = fin.read()
        eval_text = raw_text.replace('\n', '').replace("*", " ")
        sentiment_score = test_bert.evaluate_bert(eval_text)
        #TODO: this is a tmp fix because the summary score may differ greatly from the individual scores
        if cat == "Summary":
            sentiment_score = sum_of_scores/(len(categories)-1)
        else:
            sum_of_scores  += sentiment_score
        cat_feedback = []
        cat_feedback.append(cat)
        cat_feedback.append(raw_text)
        cat_feedback.append("{:.2f}%".format(sentiment_score))
        feedback_table.append(cat_feedback)

#print table
table_instance = SingleTable(feedback_table, "CodeRepro")

max_width = table_instance.column_max_width(1)
for entry in table_instance.table_data:
    wrapped_string = "\n".join(wrap(entry[1], max_width))
    entry[1] = wrapped_string

print(table_instance.table)
