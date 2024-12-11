import csv
import os

# Load positive sentiment dictionary
with open('/Users/arodriguez/Python_/Environment1/Projects and Assignments/Loughran_Mcdonald_word_list/LoughranMcDonald_Positive.csv', mode='r') as f:
    positive_wordBank = []
    for row in csv.reader(f, delimiter=','):
        positive_wordBank += row

# Load negative sentiment dictionary
with open('/Users/arodriguez/Python_/Environment1/Projects and Assignments/Loughran_Mcdonald_word_list/LoughranMcDonald_Negative.csv', mode='r') as f:
    negative_wordBank = []
    for row in csv.reader(f, delimiter=','):
        negative_wordBank += row

print("Positive words:", positive_wordBank)
print("Negative words:", negative_wordBank)

def searchWordBank(word, wordBank):
    if len(word) == 3:
        if word.upper() == 'WIN':
            return True
    elif len(word) >= 4:
        for i in wordBank:
            if word.upper() == i:
                return True
    return False

def analyzeFile(filename):
    positive_score = 0
    negative_score = 0
    company_name = os.path.splitext(os.path.basename(filename))[0]  # Extract company name from filename
    with open(filename, 'r', encoding='latin1') as file:  # Use 'latin1' encoding to handle non-UTF-8 characters
        for line in file:
            for word in line.split():
                if searchWordBank(word, positive_wordBank):
                    positive_score += 1
                if searchWordBank(word, negative_wordBank):
                    negative_score += 1
    final_score = positive_score - negative_score
    return (company_name, positive_score, negative_score, final_score)

directory = '/Users/arodriguez/Python_/Environment1/Projects and Assignments/New Articles'  # Change this to your articles directory
filenames = ['AmexCo.txt', '3M Company.txt','Apple Inc.txt','Boeing Company.txt','Caterpillar Inc.txt','Chevron Corporation.txt',
             'Cisco Systems.txt','Coca-Cola Company.txt','Dow Inc.txt','Goldman Sachs Group.txt','Home Depot.txt','Honeywell.txt',
             'IBM.txt','Intel.txt','Johnson & Johnson.txt',"McDonald.txt",'Merck & Co.txt','Microsoft.txt',
             'Nike.txt','Procter & Gamble Company.txt','Salesforce.txt','The Travelers Companies.txt','UnitedHealth Group.txt','Verizon.txt','Visa.txt',
             'Walgreens.txt','Walmart.txt','Walt Disney.txt','JPM.txt']

results = []

for x in filenames:
    file_path = os.path.join(directory, x)
    if os.path.exists(file_path):
        results.append(analyzeFile(file_path))
    else:
        print(f"File not found: {file_path}")

# Sort results by final score from highest to lowest
sorted_results = sorted(results, key=lambda x: x[3], reverse=True)

# Print sorted results
for result in sorted_results:
    print(f"{result[0]} - Positive Score: {result[1]}, Negative Score: {result[2]}, Final Score: {result[3]}")

# Print top 5 companies ranked by the total score
print("\nTop 5 companies ranked by the total score:")
for result in sorted_results[:5]:
    print(f"{result[0]} - Positive Score: {result[1]}, Negative Score: {result[2]}, Final Score: {result[3]}")
