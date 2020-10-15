"""
Evaluation of the annotated articles based on the AFP gold standard articles
"""
import jsonlines 
import pandas as pd

quantities = {"P1120":"number_of_death",
              "P1132":"number_of_participants",
              "P1339":"number_of_injured",
              "P1446":"number_of_missing",
              "P1561":"number_of_survivors",
              "P2527":"magnitude_moment_scale",
              "P2528":"magnitude_richter_scale"}

# initialize the entity and quntity annotation list in gold standard 
entity_gold, quanitty_gold = [], []

# initialize the entity and quantity statistics, number of entity and quanitty in one artilce 
entity_gold_num, quantity_gold_num = [], []

# Read the gold standard jsonlines annotations.
gold_standard_path = './gold_standard.json'
with jsonlines.open(gold_standard_path) as reader:
    for obj in reader:
        quan_temp,entity_temp = [],[]
        for label in obj["labels"]:
            if label[-1] in quantities:
                quan_temp.append(label)
            else:
                entity_temp.append(label)
        quanitty_gold.append(quan_temp)
        quantity_gold_num.append(len(quan_temp))
        entity_gold.append(entity_temp)
        entity_gold_num.append(len(entity_temp))

print("number of quantity in gold standard:")
print(quantity_gold_num)
print("number of entity in gold standard:")
print(entity_gold_num)
# initialize the entity and quntity annotation list in generated results 
entity_generated, quantity_generated = [], []
# initialize the entity and quantity statistics, number of entity and quanitty in one artilce 
entity_generated_num, quantity_generated_num = [], []
# Read the annotated jsonlines annotations 
annotated_path = './AFP_ann.json'
with jsonlines.open(annotated_path) as reader:
    for obj in reader:
        quan_temp,entity_temp = [],[]
        for label in obj["labels"]:
            if label[-1] in quantities:
                quan_temp.append(label)
            else:
                entity_temp.append(label)
        quantity_generated.append(quan_temp)
        quantity_generated_num.append(len(quan_temp))
        entity_generated.append(entity_temp)
        entity_generated_num.append(len(entity_temp))

print("number of quantity in generated results:")
print(quantity_generated_num)
print("number of entity in generated results:")
print(entity_generated_num)
# compare and statistics 
# entity_gold, entity_generated, quanitty_gold, quantity_generated have the same length and corresponding order
entity_correct_num = []
quantity_correct_num = []
for i in range(len(entity_gold)):
    # iterate through the generated entity annotations of each artilce and determine if they are in the corresponding gold standard annotations
    entity_correct_num_per_article = 0 
    for label in entity_generated[i]:
        if label in entity_gold[i]:
            entity_correct_num_per_article +=1 
    entity_correct_num.append(entity_correct_num_per_article)

    # iterate through the generated quantity annotations of each artilce and determine if they are in the corresponding gold standard annotations
    quantity_correct_num_per_article = 0 
    for label in quantity_generated[i]:
        if label in quanitty_gold[i]:
            quantity_correct_num_per_article +=1 
    quantity_correct_num.append(quantity_correct_num_per_article)

print("number of correct entity")
print(entity_correct_num)
print("number of correct quantity")
print(quantity_correct_num)

# existing csv file for the article names, schemas and wikis
csv_path = './100_gold_standard_articles.CSV'
df = pd.read_csv(csv_path)
# newly created statistics columns
df2 = pd.DataFrame({'ground_truth_entity':entity_gold_num, 'ground_truth_quantity':quantity_gold_num, 
                  'annotated_entity':entity_generated_num, '':quantity_generated_num,
                  'correct_entity':entity_correct_num,'correct_quantity':quantity_correct_num})
df = pd.concat([df,df2],axis=1)
df.to_csv(csv_path)
