import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import requests
import json
import sys
import os

def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)


api_key = "YOUR_API_KEY"
appid = "GAME_APPID"

# --- MAIN FRAME ----
root = tk.Tk()
root.title("Steam Ban/Unban Tool")

background_image = Image.open(resource_path("background.png"))
background_photo = ImageTk.PhotoImage(background_image)

root.geometry(f"{background_image.width}x{background_image.height}")

background_label = tk.Label(root, image=background_photo)
background_label.place(x=0, y=0, relwidth=1, relheight=1)

frame = tk.Frame(root, bd=0, relief="flat", bg="black")
frame.place(relx=0.5, rely=0.1, anchor="n")

#--- MAIN CODE ----

def log_message(message):
    log_box.insert(tk.END, message + "\n")
    log_box.see(tk.END)

def fetch_player_info():
    user_input = entry_steamid.get()
    steamid = resolve_steamid(user_input)
    if not steamid:
        log_message("❌ Invalid or unresolved SteamID.")
        info_text.set("Invalid SteamID.")
        return

    summary_url = f"https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v2/?key={api_key}&steamids={steamid}"
    response = requests.get(summary_url)

    if response.status_code == 200:
        players = response.json().get('response', {}).get('players', [])
        if players:
            player = players[0]
            persona_name = player.get('personaname', 'N/A')
            profile_url = player.get('profileurl', 'N/A')
            visibility = player.get('communityvisibilitystate', 'N/A')
            avatar_url = player.get('avatarfull', 'N/A')

            ban_url = f"https://api.steampowered.com/ISteamUser/GetPlayerBans/v1/?key={api_key}&steamids={steamid}"
            ban_response = requests.get(ban_url)

            if ban_response.status_code == 200:
                bans = ban_response.json().get('players', [])[0]
                vac_bans = bans.get('NumberOfVACBans', 0)
                game_bans = bans.get('NumberOfGameBans', 0)
                economy_ban = bans.get('EconomyBan', 'none')
                days_since_last_ban = bans.get('DaysSinceLastBan', -1)

                log_message("✅ Player info retrieved:")
                log_message(f" - SteamID64: {steamid}")
                log_message(f" - Name: {persona_name}")
                log_message(f" - Visibility: {visibility} (3 = Public)")
                log_message(f" - Profile Link: {profile_url}")
                log_message(f" - Avatar: {avatar_url}")
                log_message("👮 Ban history:")
                log_message(f" - VAC Bans: {vac_bans}")
                log_message(f" - Game Bans: {game_bans}")
                log_message(f" - Economy Ban: {economy_ban}")
                if days_since_last_ban != -1:
                    log_message(f" - Days since last ban: {days_since_last_ban}")
                else:
                    log_message(" - No recent bans.")
                
                info_message = (
                    f"SteamID64: {steamid}\n"
                    f"Name: {persona_name}\n"
                    f"Profile: {profile_url}\n"
                    f"Visibility: {visibility} (3 = Public)\n"
                    f"VAC Bans: {vac_bans}\n"
                    f"Game Bans: {game_bans}\n"
                    f"Economy Ban: {economy_ban}\n"
                    f"Days Since Last Ban: {days_since_last_ban if days_since_last_ban != -1 else 'No ban'}"
                )
                info_text.set(info_message)

            else:
                log_message("⚠️ Unable to retrieve ban information.")
                info_text.set("Error fetching bans.")
        else:
            log_message("❌ No player found with this SteamID.")
            info_text.set("No player found.")
    else:
        log_message(f"❌ Steam API Error: Code {response.status_code}")
        info_text.set(f"Steam API Error: {response.status_code}")

def ban_player():
    user_input = entry_steamid.get()
    steamid = resolve_steamid(user_input)
    if not steamid:
        log_message("❌ Invalid SteamID for ban.")
        return

    cheat_desc = entry_reason.get()
    is_perm = var_perm.get()
    days = entry_days.get()

    if not cheat_desc:
        log_message("❌ Please provide a reason.")
        return

    if is_perm:
        duration_seconds = 0
    else:
        if not days.isdigit():
            log_message("❌ Please enter a valid number of days.")
            return
        duration_seconds = int(days) * 86400

    report_url = 'https://partner.steam-api.com/ICheatReportingService/ReportPlayerCheating/v1/'
    report_params = {'key': api_key, 'steamid': steamid, 'appid': appid}
    report_response = requests.post(url=report_url, data=report_params)

    if report_response.status_code == 200:
        report_id = report_response.json()['response'].get('reportid')
        log_message(f"✅ Report created. ID: {report_id}")
    else:
        report_id = None
        log_message("⚠️ Report not created. Attempting direct ban.")

    ban_url = 'https://partner.steam-api.com/ICheatReportingService/RequestPlayerGameBan/v1/'
    ban_params = {
        'key': api_key,
        'steamid': steamid,
        'appid': appid,
        'cheatdescription': cheat_desc,
        'duration': duration_seconds,
        'delayban': 'false'
    }
    if report_id:
        ban_params['reportid'] = report_id

    ban_response = requests.post(url=ban_url, data=ban_params)
    if ban_response.status_code == 200:
        log_message(f"✅ Ban applied. Duration: {'Permanent' if duration_seconds == 0 else str(duration_seconds) + ' seconds'}")
    else:
        log_message(f"❌ Ban failed. {ban_response.text}")

def unban_player():
    user_input = entry_steamid.get()
    steamid = resolve_steamid(user_input)
    if not steamid:
        log_message("❌ Invalid SteamID for unban.")
        return

    unban_url = 'https://partner.steam-api.com/ICheatReportingService/RemovePlayerGameBan/v1/'
    unban_params = {'key': api_key, 'steamid': steamid, 'appid': appid}
    unban_response = requests.post(url=unban_url, data=unban_params)
    
    if unban_response.status_code == 200:
        log_message("✅ Unban applied successfully.")
    else:
        log_message(f"❌ Unban failed. {unban_response.text}")

def resolve_steamid(user_input):
    if user_input.isdigit():
        return user_input
    if "steamcommunity.com/profiles/" in user_input:
        return user_input.split("/profiles/")[1].split("/")[0]
    if "steamcommunity.com/id/" in user_input:
        custom_id = user_input.split("/id/")[1].split("/")[0]
        resolve_url = f"https://api.steampowered.com/ISteamUser/ResolveVanityURL/v1/?key={api_key}&vanityurl={custom_id}"
        response = requests.get(resolve_url)
        if response.status_code == 200:
            data = response.json()
            if data['response']['success'] == 1:
                return data['response']['steamid']
    return None

# --- UI ---
tk.Label(frame, text="SteamID64 or Steam Profile URL:", fg="white", bg="black").grid(row=0, column=0, sticky="e", padx=5, pady=5)
entry_steamid = tk.Entry(frame, width=25, bg="black", fg="white", insertbackground="white",
                         highlightthickness=1, highlightbackground="white", highlightcolor="white")
entry_steamid.grid(row=0, column=1, padx=5, pady=1)

btn_fetch = tk.Button(frame, text="Fetch Info", command=fetch_player_info, bg="darkblue", fg="white", width=10)
btn_fetch.grid(row=0, column=2, padx=1)

info_text = tk.StringVar()
tk.Label(frame, textvariable=info_text, justify="left", fg="blue", bg="black", wraplength=300).grid(row=1, column=0, columnspan=3, sticky="w", padx=5)

tk.Label(frame, text="Ban Reason:", fg="white", bg="black").grid(row=2, column=0, sticky="e", padx=5)
entry_reason = tk.Entry(frame, width=20, bg="black", fg="white", insertbackground="white",
                        highlightthickness=1, highlightbackground="white", highlightcolor="white")
entry_reason.grid(row=2, column=1, columnspan=2, padx=1, pady=5, sticky="w")

tk.Label(frame, text="Duration (in days):", fg="white", bg="black").grid(row=3, column=0, sticky="e", padx=5)
entry_days = tk.Entry(frame, width=5, bg="black", fg="white", insertbackground="white",
                      highlightthickness=1, highlightbackground="white", highlightcolor="white")
entry_days.grid(row=3, column=1, sticky="w")

def toggle_days_state():
    if var_perm.get():
        entry_days.config(state="normal")
        entry_days.delete(0, tk.END)
        entry_days.insert(0, "0")
        entry_days.config(state="readonly", fg="red", readonlybackground="black")
    else:
        entry_days.config(state="normal", fg="white", bg="black")
        entry_days.delete(0, tk.END)

var_perm = tk.BooleanVar()

chk_perm = tk.Checkbutton(
    frame, text="Permanent Ban", variable=var_perm, command=toggle_days_state,
    bg="black", fg="white", selectcolor="black",
    activebackground="black", activeforeground="white",
    relief="flat", bd=0, highlightthickness=0,
    font=("TkDefaultFont", 11), padx=10, pady=5
)
chk_perm.grid(row=5, column=0, columnspan=3, pady=(0, 10))


btn_ban = tk.Button(frame, text="Ban Player", command=ban_player, bg="red", fg="white", relief="flat", width=15)
btn_ban.grid(row=4, column=0, pady=8, padx=5, sticky="w")

btn_unban = tk.Button(frame, text="Unban Player", command=unban_player, bg="green", fg="white", relief="flat", width=15)
btn_unban.grid(row=4, column=2, pady=8, padx=5, sticky="e")

log_box = tk.Text(root, height=12, width=80, bg="black", fg="white", relief="flat")
log_box.pack(side="bottom", pady=10)

root.mainloop()




