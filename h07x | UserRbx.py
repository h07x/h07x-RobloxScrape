import requests
import sys
import json
from datetime import datetime

def fetchuserdata(username):
    print("-- roblox info scraper by h07x own")
    userid = getuserid(username)
    if not userid:
        print(f"\nfailed to fetch user data for '{username}'. the username may not exist")
        return
    data = {}
    data['profile'] = getuserprofile(userid)
    data['presence'] = getuserpresence([userid])
    data['friends'] = getuserfriends(userid)
    data['followers'] = getuserfollowers(userid)
    data['followings'] = getuserfollowings(userid)
    data['groups'] = getusergroups(userid)
    data['badges'] = getuserbadges(userid)
    data['avatar'] = getuseravatar(userid)
    data['avatarheadshot'] = getuseravatarheadshot(userid)
    data['inventory'] = getuserinventory(userid)
    data['usernamehistory'] = getusernamehistory(userid)
    data['sociallinks'] = getsociallinks(userid)
    data['creatorhub'] = getcreatorhubinfo(userid)
    data['frienddetails'] = getfrienddetails(userid)
    data['rawpresence'] = getrawpresence(userid)
    data['alts'] = findpossiblealts(userid, username)
    displayalldata(data, username)

def getuserid(username):
    urls = [
        "https://users.roblox.com/v1/usernames/users",
        "https://www.roblox.com/api/users/get-by-username?username={}".format(username)
    ]
    for url in urls:
        try:
            if "usernames/users" in url:
                payload = {"usernames": [username]}
                resp = requests.post(url, json=payload, timeout=10)
                if resp.status_code == 200:
                    users = resp.json().get('data', [])
                    if users:
                        return users[0]['id']
            else:
                resp = requests.get(url, timeout=10)
                if resp.status_code == 200:
                    data = resp.json()
                    if data.get('Id'):
                        return data['Id']
        except Exception as e:
            continue
    try:
        alturl = f"https://api.roblox.com/users/get-by-username?username={username}"
        resp = requests.get(alturl, timeout=10)
        if resp.status_code == 200:
            data = resp.json()
            if data.get('Id'):
                return data['Id']
    except:
        pass
    return None

def getuserprofile(userid):
    url = f"https://users.roblox.com/v1/users/{userid}"
    try:
        resp = requests.get(url, timeout=10)
        if resp.status_code == 200:
            return resp.json()
        else:
            return {"error": f"http {resp.status_code}"}
    except Exception as e:
        return {"error": str(e)}

def getuserpresence(userids):
    url = "https://presence.roblox.com/v1/presence/users"
    payload = {"userIds": userids}
    try:
        resp = requests.post(url, json=payload, timeout=10)
        if resp.status_code == 200:
            presences = resp.json().get('userPresences', [])
            if presences:
                return presences[0]
            else:
                return {"error": "no presence data"}
        else:
            return {"error": f"http {resp.status_code}"}
    except Exception as e:
        return {"error": str(e)}

def getuserfriends(userid):
    url = f"https://friends.roblox.com/v1/users/{userid}/friends"
    try:
        resp = requests.get(url, timeout=10)
        if resp.status_code == 200:
            data = resp.json()
            return data.get('data', [])
        else:
            return []
    except Exception as e:
        return []

def getuserfollowers(userid):
    url = f"https://friends.roblox.com/v1/users/{userid}/followers"
    try:
        resp = requests.get(url, timeout=10)
        if resp.status_code == 200:
            data = resp.json()
            return data.get('data', [])
        else:
            return []
    except Exception as e:
        return []

def getuserfollowings(userid):
    url = f"https://friends.roblox.com/v1/users/{userid}/followings"
    try:
        resp = requests.get(url, timeout=10)
        if resp.status_code == 200:
            data = resp.json()
            return data.get('data', [])
        else:
            return []
    except Exception as e:
        return []

def getusergroups(userid):
    url = f"https://groups.roblox.com/v1/users/{userid}/groups/roles"
    try:
        resp = requests.get(url, timeout=10)
        if resp.status_code == 200:
            data = resp.json()
            return data.get('data', [])
        else:
            return []
    except Exception as e:
        return []

def getuserbadges(userid):
    url = f"https://badges.roblox.com/v1/users/{userid}/badges?limit=100&sortOrder=Asc"
    try:
        resp = requests.get(url, timeout=10)
        if resp.status_code == 200:
            data = resp.json()
            return data.get('data', [])
        else:
            return []
    except Exception as e:
        return []

def getuseravatar(userid):
    url = f"https://avatar.roblox.com/v1/users/{userid}/avatar"
    try:
        resp = requests.get(url, timeout=10)
        if resp.status_code == 200:
            return resp.json()
        else:
            return {"error": f"http {resp.status_code}"}
    except Exception as e:
        return {"error": str(e)}

def getuseravatarheadshot(userid):
    url = f"https://thumbnails.roblox.com/v1/users/avatar-headshot?userIds={userid}&size=420x420&format=Png&isCircular=false"
    try:
        resp = requests.get(url, timeout=10)
        if resp.status_code == 200:
            data = resp.json()
            if data.get('data'):
                return data['data'][0]
            else:
                return {"error": "no headshot data"}
        else:
            return {"error": f"http {resp.status_code}"}
    except Exception as e:
        return {"error": str(e)}

def getuserinventory(userid):
    url = f"https://inventory.roblox.com/v1/users/{userid}/items/1?limit=10"
    try:
        resp = requests.get(url, timeout=10)
        if resp.status_code == 200:
            data = resp.json()
            return data.get('data', [])
        else:
            return []
    except Exception as e:
        return []

def getusernamehistory(userid):
    url = f"https://users.roblox.com/v1/users/{userid}/username-history?limit=10"
    try:
        resp = requests.get(url, timeout=10)
        if resp.status_code == 200:
            data = resp.json()
            return data.get('data', [])
        else:
            return []
    except Exception as e:
        return []

def getsociallinks(userid):
    socials = {'youtube': None, 'twitter': None, 'discord': None}
    url = f"https://friends.roblox.com/v1/users/{userid}/social-networks"
    try:
        resp = requests.get(url, timeout=10)
        if resp.status_code == 200:
            data = resp.json()
            for link in data.get('data', []):
                platform = link.get('platform', '').lower()
                if platform == 'youtube':
                    socials['youtube'] = link.get('address')
                elif platform == 'twitter' or platform == 'x':
                    socials['twitter'] = link.get('address')
                elif platform == 'discord':
                    socials['discord'] = link.get('address')
        return socials
    except:
        return socials

def getcreatorhubinfo(userid):
    try:
        url = f"https://create.roblox.com/v1/creators/{userid}/profile"
        resp = requests.get(url, timeout=10)
        if resp.status_code == 200:
            return resp.json()
        else:
            return {"error": "creator hub data unavailable"}
    except:
        return {"error": "creator hub data unavailable"}

def getfrienddetails(userid):
    friends = getuserfriends(userid)
    if not friends:
        return {'oldest': [], 'popular': []}
    friendswithfollowers = []
    for friend in friends[:50]:
        fid = friend.get('id')
        fname = friend.get('name', 'unknown')
        if fid:
            followers = getuserfollowers(fid)
            followercount = len(followers)
            friendswithfollowers.append({'id': fid, 'name': fname, 'followers': followercount})
    sortedbyfollowers = sorted(friendswithfollowers, key=lambda x: x['followers'], reverse=True)
    oldestfriends = []
    for friend in friends[:3]:
        oldestfriends.append({'id': friend.get('id', 'unknown'), 'name': friend.get('name', 'unknown')})
    return {'oldest': oldestfriends, 'popular': sortedbyfollowers[:3]}

def getrawpresence(userid):
    url = f"https://presence.roblox.com/v1/presence/users"
    payload = {"userIds": [userid]}
    try:
        resp = requests.post(url, json=payload, timeout=10)
        if resp.status_code == 200:
            data = resp.json()
            presences = data.get('userPresences', [])
            if presences:
                presence = presences[0]
                presencetype = presence.get('userPresenceType', 0)
                types = {0: 'offline', 1: 'online', 2: 'in game', 3: 'in studio', 4: 'invisible'}
                return {'type': types.get(presencetype, 'unknown'), 'raw': presencetype, 'lastonline': presence.get('lastOnline'), 'placeid': presence.get('placeId'), 'universeid': presence.get('universeId')}
        return {'type': 'unknown', 'raw': None}
    except:
        return {'type': 'unknown', 'raw': None}

def findpossiblealts(userid, username):
    alts = []
    try:
        followers = getuserfollowers(userid)
        for follower in followers[:30]:
            fname = follower.get('name', '')
            if fname.lower().startswith(username.lower() + '_') or fname.lower().startswith(username.lower() + '0') or fname.lower().startswith(username.lower() + '1'):
                alts.append({'name': fname, 'id': follower.get('id'), 'reason': 'similar username (follower)'})
        following = getuserfollowings(userid)
        for follow in following[:30]:
            fname = follow.get('name', '')
            if fname.lower().startswith(username.lower() + '_') or fname.lower().startswith(username.lower() + '0') or fname.lower().startswith(username.lower() + '1'):
                if not any(alt['id'] == follow.get('id') for alt in alts):
                    alts.append({'name': fname, 'id': follow.get('id'), 'reason': 'similar username (following)'})
        if len(alts) < 3:
            try:
                possiblealts = [f"{username}1", f"{username}2", f"{username}_alt", f"{username}real", f"{username}123"]
                for altname in possiblealts:
                    if len(alts) >= 3:
                        break
                    payload = {"usernames": [altname]}
                    resp = requests.post("https://users.roblox.com/v1/usernames/users", json=payload, timeout=10)
                    if resp.status_code == 200:
                        users = resp.json().get('data', [])
                        if users and users[0]['id'] != userid:
                            alts.append({'name': altname, 'id': users[0]['id'], 'reason': 'common alt naming pattern'})
            except:
                pass
        if len(alts) < 3:
            try:
                url = f"https://groups.roblox.com/v1/users/{userid}/groups/roles"
                resp = requests.get(url, timeout=10)
                if resp.status_code == 200:
                    groups = resp.json().get('data', [])
                    for group in groups[:10]:
                        if len(alts) >= 3:
                            break
                        groupid = group.get('group', {}).get('id')
                        if groupid:
                            membersurl = f"https://groups.roblox.com/v1/groups/{groupid}/users?limit=100"
                            membersresp = requests.get(membersurl, timeout=10)
                            if membersresp.status_code == 200:
                                members = membersresp.json().get('data', [])
                                for member in members:
                                    membername = member.get('user', {}).get('username', '')
                                    memberid = member.get('user', {}).get('userId')
                                    if membername.lower().startswith(username.lower()) and memberid != userid:
                                        if not any(alt['id'] == memberid for alt in alts):
                                            alts.append({'name': membername, 'id': memberid, 'reason': 'shared group membership'})
                                            break
            except:
                pass
    except:
        pass
    return alts[:3]

def displayalldata(data, username):
    print(f"\n▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰")
    print(f"            roblox profile: {username}")
    print(f"▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰")

    profile = data['profile']
    if 'error' not in profile:
        userid = profile.get('id', 'unknown')
        print(f"\n◉ user id: {userid}")
        print(f"◉ username: {profile.get('name', 'n/a')}")
        print(f"◉ display name: {profile.get('displayName', 'n/a')}")
        print(f"◉ description: {profile.get('description', 'n/a')[:200]}")
        created = profile.get('created', 'n/a')
        if created != 'n/a':
            createddate = datetime.fromisoformat(created.replace('Z', '+00:00'))
            print(f"◉ account created: {createddate.strftime('%Y-%m-%d %I:%M:%S %p')}")
            print(f"◉ creation timestamp raw: {created}")
            accountage = datetime.now().astimezone() - createddate
            print(f"◉ account age: {accountage.days} days")
        print(f"◉ is banned: {profile.get('isBanned', 'n/a')}")
        print(f"◉ has verified badge: {profile.get('hasVerifiedBadge', 'n/a')}")
    else:
        print(f"\n! profile error: {profile['error']}")

    presence = data['rawpresence']
    print(f"\n◉ presence type: {presence.get('type', 'unknown')}")
    if presence.get('placeid'):
        print(f"◉ current place id: {presence.get('placeid')}")
    if presence.get('universeid'):
        print(f"◉ current universe id: {presence.get('universeid')}")
    if presence.get('lastonline'):
        print(f"◉ last online raw: {presence.get('lastonline')}")

    print(f"\n▸ previous display names")
    history = data['usernamehistory']
    if history:
        for entry in history:
            print(f"  • {entry.get('name', 'unknown')} → changed on {entry.get('created', 'unknown')}")
    else:
        print("  • none found")

    print(f"\n▸ social links")
    socials = data['sociallinks']
    if socials.get('youtube'):
        print(f"  • youtube: {socials['youtube']}")
    if socials.get('twitter'):
        print(f"  • twitter/x: {socials['twitter']}")
    if socials.get('discord'):
        print(f"  • discord: {socials['discord']}")
    if not any(socials.values()):
        print("  • none found")

    print(f"\n▸ creator hub")
    creatorhub = data['creatorhub']
    if 'error' not in creatorhub:
        print(f"  • creator type: {creatorhub.get('creatorType', 'n/a')}")
        print(f"  • created items count: {creatorhub.get('createdItemsCount', 'n/a')}")
    else:
        print(f"  • {creatorhub.get('error')}")

    print(f"\n▸ friends & connections")
    print(f"  total friends: {len(data['friends'])}")

    oldestfriends = data['frienddetails'].get('oldest', [])
    if oldestfriends:
        print(f"  oldest friends (first 3 added):")
        for friend in oldestfriends:
            print(f"    • {friend.get('name', 'unknown')} (id: {friend.get('id', 'unknown')})")

    popularfriends = data['frienddetails'].get('popular', [])
    if popularfriends:
        print(f"  top 3 friends by follower count:")
        for friend in popularfriends:
            print(f"    • {friend.get('name', 'unknown')} (id: {friend.get('id', 'unknown')}) → {friend.get('followers', 0)} followers")

    print(f"  followers: {len(data['followers'])}")
    if len(data['followers']) > 0:
        followernames = [f.get('name', 'unknown') for f in data['followers'][:5]]
        print(f"    recent: {', '.join(followernames)}" + (" ..." if len(data['followers']) > 5 else ""))

    print(f"  following: {len(data['followings'])}")

    print(f"\n▸ possible alternative accounts")
    alts = data.get('alts', [])
    if alts:
        for alt in alts:
            print(f"  • {alt.get('name', 'unknown')} (id: {alt.get('id', 'unknown')}) → {alt.get('reason', 'unknown')}")
    else:
        print("  • none found")

    print(f"\n▸ groups ({len(data['groups'])})")
    for group in data['groups'][:5]:
        groupinfo = group.get('group', {})
        roleinfo = group.get('role', {})
        print(f"  • {groupinfo.get('name', 'unknown')} (id: {groupinfo.get('id', 'unknown')}) → {roleinfo.get('name', 'unknown')} (rank {roleinfo.get('rank', 'unknown')})")
    if len(data['groups']) > 5:
        print(f"  ... and {len(data['groups'])-5} more groups")

    print(f"\n▸ badges earned ({len(data['badges'])})")
    for badge in data['badges'][:5]:
        print(f"  • {badge.get('name', 'unknown')} → {badge.get('displayName', 'unknown')}")
    if len(data['badges']) > 5:
        print(f"  ... and {len(data['badges'])-5} more badges")

    avatar = data['avatar']
    if 'error' not in avatar:
        print(f"\n▸ avatar")
        print(f"  • type: {avatar.get('avatarType', 'unknown')}")
        print(f"  • scale: {avatar.get('playerAvatarScale', 'unknown')}")
    else:
        print(f"\n▸ avatar error: {avatar['error']}")

    avatarheadshot = data['avatarheadshot']
    if 'error' not in avatarheadshot and 'imageUrl' in avatarheadshot:
        print(f"\n▸ avatar headshot url")
        print(f"  • {avatarheadshot.get('imageUrl', 'n/a')}")
    else:
        print(f"\n▸ avatar headshot: unavailable")

    print(f"\n▸ inventory (showing first {len(data['inventory'])} items)")
    for item in data['inventory']:
        iteminfo = item.get('item', {})
        print(f"  • {iteminfo.get('name', 'unknown')} (id: {iteminfo.get('id', 'unknown')})")

    print(f"\n▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰")
    print("                     end of report")
    print("▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰\n")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("-- roblox info scraper by h07x own")
        print("usage: python h07xrblxinfo usernameofplayer")
        sys.exit(1)
    username = sys.argv[1]
    fetchuserdata(username)