# Step 1: using external database instead of sqlite

~~Unfortunately, I found MySQL wasn't installed on the PC I'm using.~~

~~So I had to install MySQL before starting the lab. TT~~

### 27th Sept

22:58
- I gonna change some lines about the connection to MySQL.
- also, some variables need to be added to the `.env` file.


23:11
- my app couldn't connect to MySQL
- it still used SQLite!! TT


23:15
- It seems I forgot some dependencies.
- ai agent is helping me install them.


23:22
- It's confirmed: the problem was missing dependencies.
- now the app's database is MySQL. 
- only 10 minutes taken 
- great ai!


23:37
- previous functions still work.
- everything seems alright (I hope so~).
- I'm gonna sleep after I commit and push.
- wish the deployment step goes as smoothly as step one.
- good night world.


23:52
- my .md doesn't perform as I expected
- try again


### 28th Sept
10:59
- database using now is in my pc localhost
- I'm trying Planetscale 


11:12
- planetscale is no more free now. TT
- go back to supabase now.


11:49
- my pc cannot reach host of supabase
- maybe it's because I choose Singapore as region? --but I didn't find hk
- I use my proxy but app still cannot work


11:56
- ai told me it was about ipv6
- my pc or network don't have ipv6 route 
- I will try my app in github codespaces


14:59
- the connection string I selected dosen't support ipv4
- and there is another connection supporting ipv4 but I didn't find it before
- why this bug can take me 3 hours?
- stupid bug and stupid me. TT


15:14
- nice! my app is now using supabase as database

### Summary/what I learnt in step 1
- since my pc won't be always on, an external database on cloud is necessary. It's a primary truth and I should have known it, but I forgot it at the beginning. as a result, I did some useless work.
- in my previous projects, I always use my own pc as server and database because I think operation on cloud would be very complex and costly, and I never try it before. But after these days' attempt, I found it really convenient!



# Step 2: deploy my app on vercel
### 28th Sept
16:12
- I sign up an account on vercel and import this repo
- but I can only use vercel for 14 days or I have to pay


18:30
- I guess I have successfully deployed this app: I can access this app in my phone while program in my vscode isn't running
- I didn't change my source code in step 2 and only 2 extra file `vercel.json` and `.vercelignore` were added
- actually there is a little question: users have to login in vercel


18:47
- now everybody can access this url without authentication
- no lines are changed in any files. just change some settings in vercel dashboard
### Summary/what I learnt in step 2
- I learnt how to deploy app on vercel
- to my surprise, I didn't change my python code in this step. everything seems to have been done in step 1 when writing logic of determining which database(sqlite, mysql or supabase) will be selected

### Step2.1: add ai into app
> I forget adding ai into my app, now I'm going to make it up
