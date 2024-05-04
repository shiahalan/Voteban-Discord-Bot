import asyncio
import discord
import re
import random
from time import sleep
from discord.utils import get


responses = (r"aye|nay|Aye|Nay|AYE|NAY")
aye_responses = ["aye", "AYE", "aYe", "Aye", "ayE", "AYe", "aYE", "AyE"]
nay_responses = ["nay", "NAY", "nAy", "Nay", "naY", "NAy", "nAY", "NaY"]

bot = discord.Client(intents = discord.Intents().all())


@bot.event
async def on_ready():  # Log into bot on run()
    print("Logged in as {0.user}".format(bot))


@bot.event
async def on_message(message):  # Message should be "Initiate judgement on [user id]"
    recorded_users = []
    recorded_responses = []
    offender_id = ""
    username = str(message.author).split("#")[0]
    user_message = str(message.content)
    channel = str(message.channel)
    id = str(message.author.id)

    print(f"{channel}: {username} says \"{user_message}\"")
    if message.author == bot.user:
        return
    else:
        if message.content.startswith("Initiate judgement") and id == "[ID of user who can start a vote ban, this stays string value]" or message.content.startswith("Initiate judgement") and id == "[ID of user who can start a vote ban, this stays string value]":
            contents = str(message.content).split()
            offender_id = contents[-1].strip()
            await message.channel.send("Searching for user with ID " + offender_id)

            try:
                int_offender_id = int(offender_id)
            except Exception:
                int_offender_id = offender_id

            finally:
              sleep(1)
              if type(int_offender_id) is not int:
                await message.channel.send("You did not provide a valid user ID to pass judgement onto. The format is as follows: Initiate judgement on [user id goes here]")
                return
            
            banned_member = get(bot.get_all_members(), id=int_offender_id)
            mod_chat = get(bot.get_all_channels(), id="[ID of channel who can start a vote ban, replace this with integer value]")

            sleep(1)
            if banned_member:
                await message.channel.send("User identified as " + str(banned_member.name))
            else:
                await message.channel.send("Invalid user ID...")
                return
                
            sleep(1)
            await message.channel.send("Initializing...")
            sleep(2)
            await message.channel.send("Listening...")
            sleep(2)
            await message.channel.send("**__MAKE SURE YOU CAREFULLY REVIEW EVIDENCE BEFORE PROCEEDING WITH MODERATOR INTERVENTION. IF ALL PARTICIPANTS DID NOT REVIEW THE EVIDENCE, PLEASE SAY \"Abstain judgement\" to hold off until evidence is reviewed!__**")
            sleep(2)
            await message.channel.send("You have two minutes to state your verdict (aye/nay) where \"aye\" is to ban and \"nay\" is to not ban!\nJudgement will be passed after **one** minutes of silence in the chat...")

            while True:
                try:
                    waiting_message = await bot.wait_for("message", check=lambda initiator: initiator.channel == message.channel, timeout=60)  # Check for people talking and start recording after initiated
                    if waiting_message.content == "Abstain judgement":
                        sleep(2)
                        await message.channel.send("Abstaining judgement for the time being...")
                        recorded_users = []
                        recorded_responses = []
                        break

                except asyncio.TimeoutError:
                    await message.channel.send("The alloted time to state your verdicts has expired. Now passing judgement...")
                    sleep(2)
                    for i in range(len(recorded_users)):
                      sleep(1)
                      await message.channel.send(recorded_users[i] + " votes " + recorded_responses[i])

                    if len(recorded_responses) < 5:  # Amount of people voting
                        sleep(2)
                        await message.channel.send("There must be at least five voters present to pass judgement!")
                        recorded_responses = []
                        recorded_users = []
                        break
                    else:
                        aye_count = 0
                        nay_count = 0

                        for i in range(len(recorded_users)):
                            if recorded_responses[i] in aye_responses:
                                aye_count += 1
                            elif recorded_responses[i] in nay_responses:
                                nay_count += 1
                            else:
                                sleep(2)
                                await message.channel.send("One of the voters passed an invalid verdict. Please either say aye or nay")
                        
                        total_count = aye_count + nay_count

                        # if aye_count >= nay_count:
                        #     await message.channel.send("The verdict is...")
                        #     await message.channel.send("GUILTY!")

                        #     break

                        if aye_count >= 5:  # Amount of people agreeing
                            sleep(2)
                            await message.channel.send("The verdict is...")
                            sleep(3)
                            await message.channel.send("**GUILTY!**")
                            recorded_responses = []
                            recorded_users = []
                            sleep(2)

                            reason = "You have been determined as guilty by the voters of [community name]...\nSubmit a ban appeal if you feel this was a mistake.\nForm: [Ban appeal form link]"
                            
                            with open("ban_record.txt", "a") as f:
                                f.write("\n" + str(banned_member.name) + " : " + str(offender_id) + "has been banned in a " + str(aye_count) + " to " + str(nay_count) + " vote!")   
                                
                            await banned_member.send(reason)
                            await banned_member.ban(reason=reason)
                            await mod_chat.send(str(banned_member.name) + " has been banned from [Server name]")
                            await message.channel.send(str(banned_member.name) + " has been banned from [Server name]")

                            break
                        else:
                            sleep(2)
                            await message.channel.send("The verdict is...")
                            sleep(3)
                            await message.channel.send("The minimum required agreement to pass a guilty verdict between voters was not met...")
                            recorded_responses = []
                            recorded_users = []
                            break
                            

                    break
                
                else:
                    valid_response = re.search(responses, waiting_message.content)

                    username = str(waiting_message.author).split("#")[0]
                    user_message = str(waiting_message.content)
                    channel = str(waiting_message.channel.name)
                    id = str(waiting_message.author.id)

                    if valid_response == None:
                        sleep(1)
                        await message.channel.send("That was not a valid verdict " + username + "...")
                        
                    elif valid_response:
                        valid_response = valid_response.string
                        sleep(1)
                        
                        if not username in recorded_users:
                            await message.channel.send(username + " says " + valid_response + "!")
                            recorded_users.append(username)
                            recorded_responses.append(valid_response.strip())
                        else:
                            await message.channel.send("You have already given your verdict " + username + "!")




bot.run("[Value of Bot Login Token, leave this as a string]")