### How It Works

  

## how to configure it

```/fast-configure-channel [#rankpoll-channel] [#rankpool-admin-channell] [disccusion-poll-channel] [discussion-pool-admin-chanell]```

**OR**

```/configure-rank-poll [#rankpoll-channel] [#rankpool-admin-channell]``` *Same Goes for discussion poll channels*

  

## How to down/upvote someone

go to the specified channel and type

```/rankvote [username] [reason] [conclussion(up-down)]```

*it will be sent to the #rankpool-admin-channell*

where an admin can approved it using this command

```/acceptvote [message-link]``` *still not sure about what is easier replying or adding the message link*

  

it will then be sent back to the #rankpoll-channel where upvotes and downvotes will be added to a database where we can make some rules like *-5 votes = downgrade*  and *+5 votes =upgrade then it gets cleared for them automatically

you can also do

```/clearvotes [username] [reason]```

## how to suggest a discussion

  
```/discussion-suggestion [dissussion-prompt] [#channel-to-discuss-in]```

*it will be sent to the #discussion-pool-admin-channel*

an admin can approve it by using  

```/acceptdiscussion [message-link]``` *still not sure about what is easier replying or adding the message link*


it will then be sent back to the discussion channel

## Admin Controlled Environment

- if the admin sees that the user is trolling admin can use ```/downvote [user]``` *which will add -1 to his record in the database* *OR* ```/downgrade [user]``` *which will downgrade him and give him a lower rank*

- if the admin sees that the user is actively contributing to the server and is worth of an upgrade he can simply ```/upvote [user]``` *which will add +1 to his record in the database* *OR* ```/upgrade [user]``` *which will upgrade him and give him a higher rank*

  
  

### Users Controlled Enviroment

  

- if a user doesn't like an admin and want to vote him out he can ```/downadmin [admin] [reason]``` *the bot will check if the mentioned admin is actually an admin or na then send it to a channel specified by the admins themselves*  

  

- if a user doesn't like a message or a video/image he can ```/report [message link] [reason]``` *it will then be sent to the same channel EX:[reports-channel]*

statistics
You can see the results and statistics of any poll using this command 
/statistics [poll message url] [chart YES/NO]
 the bot will reply with a message like this

Poll Results

Downvote: [DOWNVOTES]/[ALL VOTES]
Upvote: [UPVOTES]/[ALL VOTES]
Date: [POLL DATE]

it will also append a photo with the message with a chart depending on the Chart value in the command

ofc it will be sent as an embed with some emojis to make it prettier 
