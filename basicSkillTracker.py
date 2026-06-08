import json

with open("userData.json", "r") as f: 
    user = json.load(f)

def openSkills():
    with open("basicSkills.json", "r") as f:
        return json.load(f)
    
def updateSkills(new_list):
    with open("basicSkills.json", "w") as f:
        json.dump(new_list, f, indent=4)

def updateUser(user):
    with open("userData.json", "w") as f:
        json.dump(user, f, indent=4)

def strInput(prompt):
    while True:
        strIn = str(input(prompt)).strip()
        if strIn:
            return strIn
        else:
            print("Input cannot be empty")
        
def intInput(prompt, allowZero):
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

def addXp(val):
    user["xp"] += val
    if user["xp"] >= user["xp milestone"]:
        while user["xp"] >= user["xp milestone"]:
            user["level"] += 1
            user["xp milestone"] = (user["level"] + 1) * 100
        print(f"Congratulations, you have leveled up to level {user['level']}!")
        print(f"You need {user["xp milestone"] - user['xp']} more XP to get to level {user['level'] + 1}.")
    updateUser(user)

def progressCheck(skill, skill_list):
    if skill_list[skill]["hours"] >= skill_list[skill]["goal"]:
        print(f"Congratulations! You've reached your goal for {skill.title()}!")
        addXp(skill_list[skill]["xp value"])
        while True:
            progChoice = intInput("Would you like to (1) update your goal or (2) remove the skill from your to-do list? ", False)
            if progChoice == 1: 
                old_goal = skill_list[skill]["goal"]
                while True:
                    updated_hours = intInput("New goal: ", False)
                    if updated_hours > old_goal:
                        break
                    else:
                        print("Your new goal should be greater than your old goal, please try again")
                skill_list[skill]["goal"] = updated_hours
                skill_list[skill]["xp value"] = (updated_hours - old_goal) * 10
                updateSkills(skill_list)
                break
            elif progChoice == 2:
                del skill_list[skill]
                updateSkills(skill_list)
                user["skills mastered"] += 1
                updateUser(user)
                print("Skill mastered!")
                break
            else:
                print("Invalid choice, please try again")
    else:
        print("Your current progress in " + skill + ": ")
        print(f"   Hours Logged: {skill_list[skill]['hours']} hrs")
        print(f"   Goal: {skill_list[skill]['goal']} hrs")
        print(f"   Progress: {(skill_list[skill]['hours'] / skill_list[skill]['goal']) * 100 :.1f}%")

def skillPrint(skill_list):
    for skill, info in skill_list.items():
        print(f"\n{skill.title()}: ")
        print(f"   Hours Logged: {info['hours']} hrs")
        print(f"   Goal: {info['goal']} hrs")
        print(f"   Progress: {(info['hours'] / info['goal']) * 100 :.1f}%")
        print(f"   XP Value: {info['xp value']}")

print("Project created by Bryce Kirkwood")

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
    
    elif choice == 1:
        skill_list = openSkills()

        while True:
            new_skill_name = strInput("Name of the new skill: ").lower()
            if new_skill_name in skill_list:
                print("A skill with that name already exists, please try again")
            else:
                break
        new_skill_goal = intInput("Goal number of hours: ", False)
        new_skill_hrs = intInput("Number of hours spent so far: ", True)

        skill_list[new_skill_name] = {
                "goal": new_skill_goal,
                "hours": new_skill_hrs,
                "xp value": new_skill_goal * 10
        }
        user["hours logged"] += new_skill_hrs

        updateUser(user)
        updateSkills(skill_list)

    elif choice == 2:
        skill_list = openSkills()
        
        skillPrint(skill_list)
        while True:
            update_choice = strInput("Which skill do you want to update? ").lower()
            if update_choice not in skill_list:
                print("Skill doesn't exist, please try again")
            else:
                break

        update_hrs = intInput("Hours to add: ", True)
        skill_list[update_choice]["hours"] += update_hrs
        user["hours logged"] += update_hrs

        updateUser(user)
        updateSkills(skill_list)
        progressCheck(update_choice, skill_list)

    elif choice == 3:
        skill_list = openSkills()
        if not skill_list:
            print("You have no skills in progress")
        else:
            print(f"{user['username']}'s Active Skills: ")
            skillPrint(skill_list)

    elif choice == 4:
        skill_list = openSkills()

        if not skill_list:
            print("You have no skills to delete")
            continue

        skillPrint(skill_list)
        while True:
            del_choice = strInput("Which skill do you want to delete? ").lower()
            if del_choice not in skill_list:
                print("Skill doesn't exist, please try again")
            else:
                break
        del skill_list[del_choice]

        updateSkills(skill_list)

        print("\nHere is your new list of skills:")
        skillPrint(skill_list)

    elif choice == 5:
        print(f"{user['username']}'s Profile: ")
        for label, data in user.items():
            print(f"{label.title()}: {data}")

    elif choice == 6:
        break