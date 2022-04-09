import discord
from discord.ext import commands
import os
from urllib.parse import quote
import requests
import re
from keep_alive import keep_alive

#make connection to discord
commandsym = 'dev.'
client = discord.Client()

result_limit = 5

resources_command = ["__**Resource Commands**__", "For unity resources type the command - " + commandsym + "unity", "For art resources type the command - " + commandsym + "art", "For music resources type the command - " + commandsym + "music"]

search_command = ["__**Search Command**__", "Search github repositories in discord via the command - " + commandsym + "search (query)"]

asign_role_command = "role"

unity_resource_links = ["Unity Resources", "**Unity Forums - **", "<https://forum.unity.com/>", "**Unity Documentation - **", "<https://docs.unity3d.com/Manual/index.html>", "**Unity Manual: Scripting - **", "<https://docs.unity3d.com/Manual/ScriptingSection.html>", "**Brackeys - **", "<https://www.youtube.com/c/Brackeys>", "**Blackthornprod - **", "<https://www.youtube.com/c/Blackthornprod>"]

art_resource_links = ["Art Resources", "**Piskelapps - **", "<https://www.piskelapp.com/>", "**Gimp - **", "<https://www.gimp.org/>", "**Krita - **", "<https://krita.org/en/>", "**Jazza - **", "<https://www.youtube.com/c/Jazza>"]

music_resource_links = ["Music Resources", "**Lmms - **", "<https://lmms.io/>", "**Bosca Ceoil - **", "<https://boscaceoil.net/>", "**Audacity - **", "<https://www.audacityteam.org/>", "**Shady Cicada - **", "<https://www.youtube.com/c/Shadycicada>"]

#Registers an event
@client.event
#Called when bot is ready to be used
async def on_ready():         #This gets user
  print('We have logged in as {0.user}'.format(client))

#Triggers each time a message is recieved
@client.event 
async def on_message(message):
  if message.author == client.user:
    return
  
  msg = message.content
  msg = msg.lower()

  if msg.startswith(commandsym):
    if msg[len(commandsym):] == 'help':
      embed=discord.Embed(
      title="__**Command List**__",
        color=discord.Color.green())
      rc_str = ""
      for i in range(1, len(resources_command)):
        rc_str += resources_command[i] + '\n'
      embed.add_field(name=resources_command[0], value=rc_str, inline=False)

      sc_str = ""
      for i in range(1, len(search_command)):
        sc_str += search_command[i] + '\n'
      embed.add_field(name=search_command[0], value=sc_str, inline=False)
      await message.channel.send(embed=embed)

      #one_word_per_line = '\n'.join(resources_command)
      #quote_text = '\n>>> {}'.format(one_word_per_line)
      #await message.channel.send(quote_text)
    elif msg[len(commandsym):] == 'unity':
      embed=discord.Embed(
      title="__**" + unity_resource_links[0] + "**__",
        color=discord.Color.green())
      temp_str = ""
      for i in range(2, len(unity_resource_links)):
        temp_str += unity_resource_links[i] + '\n'
      embed.add_field(name=unity_resource_links[1], value=temp_str, inline=False)
      await message.channel.send(embed=embed)
    elif msg[len(commandsym):] == 'art':
      embed=discord.Embed(
      title="__**" + art_resource_links[0] + "**__",
        color=discord.Color.green())
      temp_str = ""
      for i in range(2, len(art_resource_links)):
        temp_str += art_resource_links[i] + '\n'
      embed.add_field(name=art_resource_links[1], value=temp_str, inline=False)
      await message.channel.send(embed=embed)
    elif msg[len(commandsym):] == 'music':
      embed=discord.Embed(
      title="__**" + music_resource_links[0] + "**__",
        color=discord.Color.green())
      temp_str = ""
      for i in range(2, len(music_resource_links)):
        temp_str += music_resource_links[i] + '\n'
      embed.add_field(name=music_resource_links[1], value=temp_str, inline=False)
      await message.channel.send(embed=embed)
    
  if msg.startswith(commandsym + "search"):
    url_start = "https://api.github.com/search/repositories?q="
    url_query = msg[11:]
    url_build_query = "{" + quote(url_query) + "}"
    url = url_start + url_build_query

    #Gets the json file from GitHub to pull information from
    json_array = requests.get(url).text

    #Pull from json_array and get Github urls
    urls_list = get_github_variable("html_url", json_array, result_limit * 2)

    urls_fixed = []
    counter = 0
    for i in urls_list:
      if counter >= 1:
        urls_fixed.append(i)
        counter = 0
      else:
        counter += 1

    #Pull from json_array and get Github descriptions
    desc_list = get_github_variable("description", json_array, result_limit)

    #Pull from json_array and get Github names
    names_list = get_github_variable("full_name", json_array, result_limit)

    #Compile all the information into a single string to output into discord

    embed=discord.Embed(
    title="__**Github Search**__",
      color=discord.Color.green())
    for i in range(0, len(names_list)):
      embed.add_field(name='__**' + names_list[i] + '**__', value=desc_list[i] + '\n' + urls_fixed[i], inline=False)
    await message.channel.send(embed=embed)

def get_github_variable(gitvar, gitjson, maxresults):
  #json_git_url holds the wanted variable
  json_git_var = gitvar
  count = 0

  json_list = []
  #Searches for every html_url variable and gets the GitHub url
  for i in re.finditer(json_git_var, gitjson):
    end = i.end() + 3
    #print("beggining - " + str(end))
    #print(json_array[end:end+100])
    index_cut_off = gitjson[end:].find(",")
    #print(json_array[end:end+index_cut_off-1])
    json_list.append(gitjson[end:end+index_cut_off-1]) 
    count += 1

    if count >= maxresults:
      return json_list
  
  return json_list

keep_alive()
client.run(os.getenv('TOKKEN'))