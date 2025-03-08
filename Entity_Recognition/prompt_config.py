#prompt configuration
def get_few_shot_prompt(question):
    """
    Returns a prompt with few-shot examples for the LLM.
    """
    prompt = f"""
Your task is to process the given question and:
1. Identify entities that are culturally specific and might vary between cultures. These entities may include names of people, places, currencies and currency symbols, cooking items, and other culturally relevant elements.
2. Replace each identified cultural entity in the question with a placeholder enclosed in curly braces, indicating the type of entity (e.g., {{Person name}}, {{place}}, {{currency}}, {{cooking_item}}).
Please only identify and replace cultural entities, and retain all numerical values and mathematical logic exactly as they are.

Output Format:

First, list the entities under Entities Identified:.
Then, provide the modified question under GSM Symbolic:
Do not include any extra text or repeat sections.
Refer to the examples provided for clarification.

### Example 1:
Question: Janet's ducks lay 16 eggs per day. She eats three for breakfast every morning and bakes muffins for her 
friends every day with four. She sells the remainder at the farmers' market daily for $2 per fresh duck egg. How much in 
dollars does she make every day at the farmers' market?

Entities Identified:
- Person Name: Janet
- Types of commercial markets: farmers' market
- Currency: Dollars
- Currency sign: $
- food items: muffins
- Cooking method: Baking

GSM Symbolic:
Question: {Person name} ducks lay 16 eggs per day. She eats three for breakfast every morning and bakes
{food items} for her friends every day with four. She sells the remainder at the {Types of commercial markets} daily for 
{currency sign} 2 per fresh duck egg. How much in {currency} does she make every day at {Types of commercial markets}?

----
### Example 2:
Question: John takes 2 bolts of blue fiber and half that much white fiber.  How many bolts in total does it take?

Entities Identified:
- Person name: John

GSM Symbolic:
Question: A {{Person name}} takes 2 bolts of fiber and half that much white fiber.  How many bolts in total does it take?
How many bolts in total does it take?

----
### Example 3:
Question: Josh decides to try flipping a house.  He buys a house for $80,000 and then puts in $50,000 in repairs.
This increased the value of the house by 150%.  How much profit did he make?

Entities Identified:
- Person name: Josh
- Currency: Dollars
- Currency sign: $

GSM Symbolic:
Question: {{Person name}} decides to try flipping a house.  He buys a house for {{currency sign}}80,000 and then puts in {{currency sign}}50,000 in repairs.
This increased the value of the house by 150%.  How much profit did he make?

----
### Example 4:
Question: James decides to run 3 sprints 3 times a week.  He runs 60 meters each sprint.  How many total meters does he run a week?

Entities Identified:
- Person name: James

GSM Symbolic:
Question: {{Person name}} decides to run 3 sprints 3 times a week.  He runs 60 meters each sprint.
How many total meters does he run a week?

----
### Example 5:
Question: Eliza's rate per hour for the first 40 hours she works each week is $10. She also receives an overtime pay of 1.2 times her 
regular hourly rate. If Eliza worked for 45 hours this week, how much are her earnings for this week?

Entities Identified:
- Person name: Eliza
- Currency: Dollars
- Currency sign: $

GSM Symbolic:
Question: {{Person name}} rate per hour for the first 40 hours she works each week is {{currency sign}}10. 
She also receives an overtime pay of 1.2 times her regular hourly rate. If {{Person name}} worked for 45 hours this week, 
how much are her earnings for this week?

----
### Example 6:
Question: Two trains leave San Rafael at the same time. They begin traveling westward, both traveling for 80 miles.
The next day, they travel northwards, covering 150 miles. What's the distance covered by each train in the two days?

Entities Identified:
- Place name: San Rafael

GSM Symbolic:
Question: Two trains leave {{place name}} at the same time. They begin traveling westward, both traveling for 80 miles. 
The next day, they travel northwards, covering 150 miles. What's the distance covered by each train in the two days?

----
### Example 7:
Question: Melanie is a door-to-door saleswoman. She sold a third of her vacuum cleaners at the green house, 
2 more to the red house, and half of what was left at the orange house. If Melanie has 5 vacuum cleaners left, 
how many did she start with?

Entities Identified:
- Name: Melanie
- Types of houses: green house, red house, orange house
- Types of jobs men and women have: door-to-door saleswoman

GSM Symbolic:
Question: {{name}} is a {{Types of jobs men and women have}}. She sold a third of her vacuum cleaners at the {{Types of houses}},
2 more to the {{Types of houses}}, and half of what was left at the {{Types of houses}}. If {{name}} has 5 vacuum cleaners left, 
how many did she start with?
---

Now process the following question:
Question:
{question}
"""return prompt
