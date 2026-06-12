import json
import sqlite3
import os

# Creates a user data JSON file if one doesn't exist
if not os.path.exists("userData.json"):
    default_user = {
        "username": None,
        "xp": 0,
        "level": 0,
        "xp milestone": 100,
        "skills mastered": 0,
        "hours logged": 0
    }
    with open("userData.json", "w") as f:
        json.dump(default_user, f, indent=4)

with open("userData.json", "r") as f: 
    user = json.load(f)

def updateUser(user): # Commits any changes made to userData
    with open("userData.json", "w") as f:
        json.dump(user, f, indent=4)

def addXp(val): # Adds xp to userData and checks for level-ups
    user["xp"] += val
    if user["xp"] >= user["xp milestone"]:
        while user["xp"] >= user["xp milestone"]:
            user["level"] += 1
            user["xp milestone"] = (user["level"] + 1) * 100
        print(f"Congratulations, you have leveled up to level {user['level']}!")
        print(f"You need {user["xp milestone"] - user['xp']} more XP to get to level {user['level'] + 1}.")
    updateUser(user)

def strInput(prompt): # Handles user string input
    while True:
        strIn = str(input(prompt)).strip()
        if strIn:
            return strIn
        else:
            print("Input cannot be empty")
        
def intInput(prompt, allowZero): # Handles user int input
    while True:
        try:
            intIn = int(input(prompt))
        except ValueError:
            print("Invalid input, please try again")
        else:
            if allowZero == False and intIn == 0:
                print("Invalid input, please try again")
            elif intIn < 0:
                print("Invalid input, please try again")
            else:
                return intIn

def getSkills(): # Returns all rows from the skills table
    with sqlite3.connect("skills.db") as conn:
        cursor = conn.cursor()
        cursor.execute("""SELECT * FROM skills""")
        skills = cursor.fetchall()
    return skills

def getSkill(name): # Returns a single row from the skills table
    with sqlite3.connect("skills.db") as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT hours, goal, xp_value
            FROM skills
            WHERE name = ?
            """, (name,))
        return cursor.fetchone()

def addSkill(name, goal, hours): # Adds a new skill to the skills table
    with sqlite3.connect("skills.db") as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO skills
            (name, goal, hours, xp_value)
            VALUES (?, ?, ?, ?)
            """, (name, goal, hours, goal * 10))

def deleteSkill(del_choice): # Deletes a skill from the skills table
    with sqlite3.connect("skills.db") as conn:
        cursor = conn.cursor()
        cursor.execute("""
        DELETE FROM skills
        WHERE name = ?
        """, (del_choice,))

def progressSkill(name, addHours): # Adds hours towards competing a skill
    with sqlite3.connect("skills.db") as conn:
        cursor = conn.cursor()
        cursor.execute("""
        UPDATE skills
        SET hours = hours + ?
        WHERE name = ?
        """, (addHours, name))

def progressCheck(skillName): # Checks if a user has completed a skill and handles nect steps
    row = getSkill(skillName)
    if row[0] >= row[1]:
        print(f"Congratulations! You've reached your goal for {skillName}!")
        addXp(row[2])
        while True:
            progChoice = intInput("Would you like to (1) update your goal or (2) remove the skill from your to-do list? ", False)

            if progChoice == 1: 
                old_goal = row[1]
                while True:
                    updated_hours = intInput("New goal: ", False)
                    if updated_hours > old_goal:
                        break
                    else:
                        print("Your new goal should be greater than your old goal, please try again")
                with sqlite3.connect("skills.db") as conn:
                    cursor = conn.cursor()
                    cursor.execute("""
                        UPDATE skills
                        SET goal = ? 
                        WHERE name = ?
                        """, (updated_hours, skillName))
                    cursor.execute("""
                        UPDATE skills 
                        SET xp_value = ? 
                        WHERE name = ?""", ((updated_hours - old_goal) * 10, skillName))
                row = getSkill(skillName)
                break

            elif progChoice == 2:
                deleteSkill(skillName)
                user["skills mastered"] += 1
                updateUser(user)
                print("Skill mastered!")
                break

            else:
                print("Invalid choice, please try again")
    else:
        print("Your current progress in " + skillName + ": ")
        print(f"   Hours Logged: {row[0]} hrs")
        print(f"   Goal: {row[1]} hrs")
        if row[1] != 0:
            print(f"   Progress: {(row[0] / row[1]) * 100 :.1f}%")
        else:
            print("   Error calculating progress percentage, goal is 0")

def skillExistence(skillName): # Returns True if skillName exists and False otherwise
    with sqlite3.connect("skills.db") as conn:
        cursor = conn.cursor()
        cursor.execute("""SELECT EXISTS(SELECT 1 FROM skills WHERE name = ?)""", (skillName,))
        existence = cursor.fetchone()[0]
    return existence == 1

def checkEmptyList(): # Returns 0 if there are no skills and >0 otherwise
    with sqlite3.connect("skills.db") as conn:
        cursor = conn.cursor()
        cursor.execute("""SELECT COUNT(*) FROM skills""")
        empty = cursor.fetchone()[0]
    return empty

def skillPrint(): # Prints data from the skills table in a readable format
    skills = getSkills()
    for name, goal, hours, xp_value in skills:
        print(f"\n{name.title()}: ")
        print(f"   Hours Logged: {hours} hrs")
        print(f"   Goal: {goal} hrs")
        if goal != 0:
            print(f"   Progress: {(hours / goal) * 100 :.1f}%")
        else:
            print("   Error calculating progress percentage, goal is 0")
        print(f"   XP Value: {xp_value}")

# Prompts the user to create a simple account when a new user data file is created
if user["username"] == None:
    username = strInput("It appears this is your first time here, please enter a username: ")
    user["username"] = username
    updateUser(user)

print(f"Hello {user['username']}, and welcome to your skill tracker!")

while True:
    print("\nWhat would you like to do?")
    print("1. Add a New Skill " \
        "\n2. Log Progress on a Skill " \
        "\n3. View all Skills " \
        "\n4. Delete a Skill " \
        "\n5. View Profile" \
        "\n6. Exit")
    
    choice = intInput("Enter the number corresponding to your choice: ", False)

    if choice < 1 or choice > 6:
        print("No option corresponds to input, please try again")
        continue
    
    elif choice == 1: # Add a new skill -------------------------------------
        while True:
            new_skill_name = strInput("Name of the new skill: ").lower()
            if skillExistence(new_skill_name):
                print("A skill with that name already exists, please try again")
            else:
                break
        new_skill_goal = intInput("Goal number of hours: ", False)
        new_skill_hrs = intInput("Number of hours spent so far: ", True)

        addSkill(new_skill_name, new_skill_goal, new_skill_hrs)
        user["hours logged"] += new_skill_hrs

        updateUser(user)

    elif choice == 2: # Make progress on a skill ----------------------------
        skillPrint()
        while True:
            update_choice = strInput("Which skill do you want to update? ").lower()
            if not skillExistence(update_choice):
                print("Skill doesn't exist, please try again")
            else:
                break

        update_hrs = intInput("Hours to add: ", True)
        progressSkill(update_choice, update_hrs)
        user["hours logged"] += update_hrs

        updateUser(user)
        progressCheck(update_choice)

    elif choice == 3: # View all skills -------------------------------------
        if checkEmptyList() == 0:
            print("You have no skills in progress")
        else:
            print(f"{user['username']}'s Active Skills: ")
            skillPrint()

    elif choice == 4: # Delete a skill --------------------------------------
        if checkEmptyList() == 0:
            print("You have no skills to delete")
            continue
        skillPrint()
        while True:
            del_choice = strInput("Which skill do you want to delete? ").lower()
            if not skillExistence(del_choice):
                print("Skill doesn't exist, please try again")
            else:
                break
        deleteSkill(del_choice)
        print("\nHere is your new list of skills:")
        skillPrint()

    elif choice == 5: # View profile ----------------------------------------
        print(f"{user['username']}'s Profile: ")
        for label, data in user.items():
            print(f"{label.title()}: {data}")

    elif choice == 6: # Exit
        break