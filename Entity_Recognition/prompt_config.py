#prompt configuration
def get_few_shot_prompt(question):
    """
    Returns a prompt with few-shot examples for the LLM.
    """
    prompt = f"""
Your task is to process the given question and:

1. **Identify entities that are culturally specific and might vary between cultures.** These entities may include names of people, places, currencies and currency symbols, cooking items, and other culturally relevant elements.

2. **Replace each identified cultural entity in the question with a placeholder enclosed in curly braces**, indicating the type of entity (e.g., {{name}}, {{place}}, {{currency}}, {{cooking_item}}).

Please **only** identify and replace cultural entities, and **retain all numerical values and mathematical logic exactly as they are**.

**Output Format:**

First, list the entities under **Entities Identified:**.

Then, provide the modified question under **GSM Symbolic:**.

Do **not** include any extra text or repeat sections.

Refer to the examples provided for clarification.

Refer to the examples provided for clarification.

### Example 1:
Question: Janet's ducks lay 16 eggs per day. She eats three for breakfast every morning and bakes muffins for her 
friends every day with four. She sells the remainder at the farmers' market daily for $2 per fresh duck egg. How much in 
dollars does she make every day at the farmers' market?

Answer: Janet sells 16 - 3 - 4 = <<16-3-4=9>>9 duck eggs a day.
She makes 9 * 2 = $<<9*2=18>>18 every day at the farmer's market.
#### 18

Entities Identified:
- Name: Janet
- Types of commercial markets: farmers' market
- Currency: Dollars
- Currency sign: $
- Eating items in breakfast: muffins
- Cooking method: Baking

GSM Symbolic:
Question: {{name}} ducks lay 16 eggs per day. She eats three for breakfast every morning and {{cooking method}} 
{{eating items in breakfast}} for her friends every day with four. She sells the remainder at the {{Types of commercial markets}} daily for 
{{currency sign}} 2 per fresh duck egg. How much in {{currency}} does she make every day at {{Types of commercial markets}}?

----


### Example 2:
Question: A robe takes 2 bolts of blue fiber and half that much white fiber.  How many bolts in total does it take?

Answer: It takes 2/2=<<2/2=1>>1 bolt of white fiber
So the total amount of fabric is 2+1=<<2+1=3>>3 bolts of fabric
#### 3

Entities Identified:
- Name: robe
- Common construction elements names: blue fiber, white fiber

GSM Symbolic:
Question: A {{name}} takes 2 bolts of {{Common construction elements names}} and half that much  {{Common construction elements names}}.
How many bolts  in total does it take?

----


### Example 3:
Question: Josh decides to try flipping a house.  He buys a house for $80,000 and then puts in $50,000 in repairs.
This increased the value of the house by 150%.  How much profit did he make?

Answer: The cost of the house and repairs came out to 80,000+50,000=$<<80000+50000=130000>>130,000
He increased the value of the house by 80,000*1.5=<<80000*1.5=120000>>120,000
So the new value of the house is 120,000+80,000=$<<120000+80000=200000>>200,000
So he made a profit of 200,000-130,000=$<<200000-130000=70000>>70,000
#### 70000

Entities Identified:
- Name: Josh
- Currency: Dollars
- Currency sign: $

GSM Symbolic:
Question: {{name}} decides to try flipping a house.  He buys a house for {{currency sign}}80,000 and then puts in {{currency sign}}50,000 in repairs.
This increased the value of the house by 150%.  How much profit did he make?

----


### Example 4:
Question: James decides to run 3 sprints 3 times a week.  He runs 60 meters each sprint.  How many total meters does he run a week?

Answer: He sprints 3*3=<<3*3=9>>9 times
So he runs 9*60=<<9*60=540>>540 meters
#### 540

Entities Identified:
- Name: James

GSM Symbolic:
Question: {{name}} decides to run 3 sprints 3 times a week.  He runs 60 meters each sprint.
How many total meters does he run a week?

----

### Example 5:
Question: Eliza's rate per hour for the first 40 hours she works each week is $10. She also receives an overtime pay of 1.2 times her 
regular hourly rate. If Eliza worked for 45 hours this week, how much are her earnings for this week?

Answer: Eliza is entitled to 45 -40 = <<45-40=5>>5 hours overtime pay.
Her hourly rate for the overtime pay is $10 x 1.2 = $<<10*1.2=12>>12.
So, Eliza will receive $12 x 5 =$<<12*5=60>>60 for overtime pay.
Her regular weekly earning is $10 x 40 = $<<10*40=400>>400.
Thus, Eliza will receive a total of $400 + $60 = $<<400+60=460>>460 for this week's work.
#### 460

Entities Identified:
- Name: Eliza
- Working structure: rate per hour
- Currency: Dollars
- Currency sign: $

GSM Symbolic:
Question: {{name}} {{working structure}} for the first 40 hours she works each week is {{currency sign}}10. 
She also receives an overtime pay of 1.2 times her regular hourly rate. If Eliza worked for 45 hours this week, 
how much are her earnings for this week?

----

### Example 6:
Question: Two trains leave San Rafael at the same time. They begin traveling westward, both traveling for 80 miles.
The next day, they travel northwards, covering 150 miles. What's the distance covered by each train in the two days?

Answer: On the first day, the trains covered 2 trains * 80 miles/train = <<2*80=160>>160 miles together.
They also covered 150 miles/train * 2 trains = <<150*2=300>>300 miles together on the second day.
The combined distance the two trains covered in the two days is 300 miles + 160 miles = <<300+160=460>>460 miles
The average distance for the two days is 460 miles / 2 trains = <<460/2=230>>230 miles/train
#### 230

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

Answer: First multiply the five remaining vacuum cleaners by two to find out how many Melanie had before she visited the orange house: 
5 * 2 = <<5*2=10>>10. Then add two to figure out how many vacuum cleaners she had before visiting the red house: 10 + 2 = <<10+2=12>>12
Now we know that 2/3 * x = 12, where x is the number of vacuum cleaners Melanie started with. 
We can find x by dividing each side of the equation by 2/3, which produces x = 18
#### 18

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
"""
    return prompt
