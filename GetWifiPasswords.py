import subprocess
import re


def get_saved_wifi_profiles():
    command_output = subprocess.run(
        ["netsh", "wlan", "show", "profile"], capture_output=True, text=True).stdout
    profiles = re.findall(r"All User Profile\s*:\s*(.*)", command_output)
    return profiles


def get_wifi_password(profile_name):
    profile_info = subprocess.run(["netsh", "wlan", "show", "profile",
                                  f"name={profile_name}", "key=clear"], capture_output=True, text=True).stdout
    password_match = re.search(r"Key Content\s*:\s*(.*)", profile_info)

    if password_match:
        return password_match.group(1)
    return None


if __name__ == "__main__":
    wifi_profiles = get_saved_wifi_profiles()

    for profile in wifi_profiles:
        password = get_wifi_password(profile)

        if password:
            print(f"SSID: {profile} | Password: {password}")
        else:
            print(f"SSID: {profile} | Password: Not found")

    input("Press any key to exit...")
