# coding: utf-8

"""
Runs a series of SQL queries on the RPG game database rpg_db.sqlite3,
as per the questions in the Readme (LSDS 321 Assignment).
"""


# ## **Setup: Setting up the SQLite DB:**
import sqlite3
import pandas as pd


# Open up a new connection:
conn = sqlite3.connect('rpg_db.sqlite3')


# Open new cursor:
curs = conn.cursor()


# Assignment - Part 1, Querying a Database:

# This directory contains a file rpg_db.sqlite3, a database for a hypothetical
# webapp role-playing game. This test data has dozens-to-hundreds of randomly
# generated characters across the base classes (Fighter, Mage, Cleric, and
# Thief) as well as a few Necromancers. Also generated are Items, Weapons,
# and connections from characters to them. Note that, while the name field
# was randomized, the numeric and boolean fields were left as defaults.
#
# Use sqlite3 to load and write queries to explore the data, and answer the
# following questions:


# (1) How many total Characters are there?

num_characters = curs.execute("""SELECT COUNT(DISTINCT character_id)
                            FROM charactercreator_character"""
                        ).fetchall()[0][0]
print(f"\n(1) How many total Characters are there?: {num_characters} Chars.")


# (2) How many characters of each specific subclass are there?
print("\n(2) How many of each specific subclass (of Character)?")

# SQLite queries to find how many unique characters there are of each
# character type:
num_clerics = curs.execute("""SELECT COUNT(DISTINCT character_ptr_id)
                              FROM charactercreator_cleric"""
                          ).fetchall()[0][0]

num_fighters = curs.execute("""SELECT COUNT(DISTINCT character_ptr_id)
                               FROM charactercreator_fighter"""
                           ).fetchall()[0][0]

num_thiefs = curs.execute("""SELECT COUNT(DISTINCT character_ptr_id)
                             FROM charactercreator_thief"""
                         ).fetchall()[0][0]

num_mages = curs.execute("""SELECT COUNT(DISTINCT character_ptr_id)
                            FROM charactercreator_mage"""
                        ).fetchall()[0][0]

num_mages_necromancers = curs.execute("""SELECT COUNT(DISTINCT mage_ptr_id)
                                         FROM charactercreator_necromancer"""
                                     ).fetchall()[0][0]

# Print answers:
print(f"# of clerics: {num_clerics}")
print(f"# of fighters: {num_fighters}")
print(f"# of thiefs: {num_thiefs}")
print(f"# of mages: {num_mages} (incl. {num_mages_necromancers} necromancers)")

# Check to make sure we covered all characters and type:
assert num_characters == num_clerics + num_fighters + num_thiefs + num_mages


# (3) How many total Items?**
print("\n(3) How many total Items?")

# SQLite queries to find how many unique items, how many of those are weapons,
# and how many total items held by characters there are:
num_unique_items = curs.execute("""SELECT COUNT(DISTINCT item_id)
                                   FROM armory_item"""
                               ).fetchall()[0][0]

num_weapons = curs.execute("""SELECT COUNT(DISTINCT item_ptr_id)
                              FROM armory_weapon"""
                          ).fetchall()[0][0]

total_items_held = curs.execute("""SELECT COUNT(item_id)
                                   FROM charactercreator_character_inventory"""
                               ).fetchall()[0][0]

# Print answers:
print(f"""# of unique item types: {num_unique_items} items ({num_weapons} weapons, {num_unique_items - num_weapons} non-weapons)""")
print(f"# of total items held by characters: {total_items_held} items")


# (4) How many of the Items are weapons? How many are not?
print("\n(4) How many of the Items are weapons? How many are not?")

# Already printed with answer to Question #3 above.
print("Already printed in answer to Question #3 above.")


# (5) How many Items does each character have? (Return first 20 rows)
print("\n(5) How many Items does each character have? (Return first 20 rows)")

# SQLite query to find how many total items each character has:
query_05_results = curs.execute("""SELECT character_id, COUNT(item_id)
                                   FROM charactercreator_character_inventory
                                   GROUP BY character_id
                                   ORDER BY character_id
                                   LIMIT 20"""
                               ).fetchall()

# Display results as a table by making into a pandas dataframe:
q5_results_df = pd.DataFrame(query_05_results,
             columns=['character_id', 'num_items_held'])
q5_results_df           # Display if in notebook.
print(q5_results_df)    # Print results if in command line.


# (6) How many Weapons does each character have? (Return first 20 rows)
print("\n(6) How many Weapons does each character have? (Return first 20 rows)")

# SQLite query to find how many weapons each character has:
query_06_results = curs.execute("""
            SELECT inventory.character_id, COUNT(inventory.item_id)
            FROM charactercreator_character_inventory AS inventory
            WHERE inventory.item_id IN (SELECT item_ptr_id FROM armory_weapon)
            GROUP BY inventory.character_id"""
        ).fetchall()

# Display results as a table by making into a pandas dataframe:
q6_results_df = pd.DataFrame(query_06_results,
                             columns=['character_id', 'num_weapons_held'])
q6_results_df           # Display if in notebook.
print(q6_results_df)    # Print results if in command line.

# CHECK answer (BUT don't use this syntax -- BETWEEN 138 AND 174 isn't as
# good as directly checking if item_id is in weapons):
curs.execute("""SELECT character_id,
                COUNT(item_id)
                FROM charactercreator_character_inventory
                WHERE item_id BETWEEN 138 AND 174
                GROUP BY character_id
                ORDER BY character_id
                LIMIT 20"""
            ).fetchall()


# (7) On average, how many Items does each Character have?
print("\n(7) On average, how many Items does each Character have?")

# SQLite query to find avg. # of items held per character:
avg_items_per_character = curs.execute("""
        SELECT CAST(COUNT(item_id) AS FLOAT) / COUNT(DISTINCT character_id)
        FROM charactercreator_character_inventory"""
        ).fetchall()[0][0]

# Print answer:
print(f"Avg. # items held per character: {avg_items_per_character:.2f} items")

# CHECK answer:
# Avg. items per character: 898 total items / 302 chars. = 2.9735099337748343
assert avg_items_per_character == total_items_held / num_characters == 898/302


# (8) On average, how many Weapons does each character have?
print("\n(8) On average, how many Weapons does each character have?")

# Execute SQLite query to find avg. # weapons held per character (all chars.):
avg_weap_per_char = curs.execute("""
SELECT CAST(COUNT(item_id) AS FLOAT)
/ (SELECT COUNT(DISTINCT character_id) FROM charactercreator_character_inventory)
FROM charactercreator_character_inventory as inventory
WHERE item_id IN (SELECT item_ptr_id FROM armory_weapon)"""
).fetchall()[0][0]

# Print answer:
print(f"Avg. # of weapons per character: {avg_weap_per_char:.2f} weapons")

# CHECK answer:
# Avg. weapons per character (all characters):
# 203 total weapons held / 302 characters = 0.6721854304635762
assert avg_weap_per_char == 203 / 302


# Execute SQLite query to find avg. # weapons per weapon-holding character:
avg_weap_per_weap_holder = curs.execute("""
            SELECT CAST(COUNT(item_id) AS FLOAT) / COUNT(DISTINCT character_id)
            FROM charactercreator_character_inventory
            WHERE item_id IN (SELECT item_ptr_id FROM armory_weapon)"""
        ).fetchall()[0][0]

# Print answer:
print(f"""Avg. # of weapons per weapon-holding character:
          {avg_weap_per_weap_holder:.2f} weapons""")

# CHECK answer:
# Avg. weapons per weapon-holding character:
# 203 weapons held / 155 weapon-holding characters = 1.3096774193548386
assert avg_weap_per_weap_holder == 203 / 155
