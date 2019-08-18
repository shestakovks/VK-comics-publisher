# VK comics publisher

Python3 project that downloads random [xkcd](https://xkcd.com/) comics and posts it to your VK group wall.


## How to install

1. First of all you need to register at [VK](https://vk.com/), if you still haven't.
2. Go to your [Groups](https://vk.com/groups) and click [Create community](https://vk.com/groups_create) button up top. You can now see your new group under [Managed comunities](https://vk.com/groups?tab=admin) tab in your Groups. Now, go [here](http://regvk.com/id/) and paste your group link to the field presented, click button and then copy numbers under "ID публичной страницы" field. This is your ```group_id```
3. Now, you need to register your app on [VK dev](https://vk.com/dev). Click "My Apps" link on top of the page. Fill your form with somewhat realistic information if possible. As you choose platform, I recommend "Standalone app" which best represents this program.
4. After creation of your app, return to [My apps](https://vk.com/apps?act=manage) and click "Manage" near your app. At your address bar you'll see your ```client_id```.
5. Then you need to get your VK token. Just follow the instructions on [this](https://vk.com/dev/implicit_flow_user) page (couple advice: a) don't use redirect_uri; b) under scope parameter you need - photos, groups, wall and offline, you can list them comma separated, like this - scope=photos,groups.) You can also use following link (replace XXXXXX with client_id you acquired before). After this, new page will show, and in your address bar will be your ```access_token```.
```
https://oauth.vk.com/authorize?client_id=XXXXXX&display=page&scope=photos,groups,wall,offline&response_type=token&v=5.101
``` 

6. Now you need to create ```.env``` file in directrory with this program and put there your group_id, client_id, access_token, and api_version, which is 5.101. ```.env``` file should look like this, but with your data instead:
```
VK_CLIENT_ID=7141771
VK_ACCESS_TOKEN=a654q37a956624d19591d7ee1f6cef69e1f868663b34351hm567ffd6e2f4ke17f034946092bd8dcf44b32
VK_API_VERSION=5.101
VK_GROUP_ID=184428539
```

7. Python3 should be already installed. The script was made using `Python 3.7.3`. This version or higher should be fine.

8. Then use `pip` (or `pip3`, if there is a conflict with Python2) to install dependencies:
```
pip install -r requirements.txt
```

## How to use

Usage is really simple, opposed to settings :)

```
$ python3 main.py 
Comics: "worst_case_scenario.png" was successfully posted.
```
Result - check the [screenshot](https://i.imgur.com/IG7VdkV.png)

## Project Goals

The code is written for educational purposes on online-course for web-developers [dvmn.org](https://dvmn.org/).
