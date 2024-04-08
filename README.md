# FreeDNS Alt Creator

### Uses Temporary Emails + `freedns-client` to automatically make activated FreeDNS alts.
> You will need to manually fill out the Human Verification, the rest is automated.

Accounts are listed in accounts.txt

If you're using replit, set an environment variable (`REP_OWNER`) to your username, to make sure that people can't fork your accounts.txt or use it. (Also, if you're using replit, don't use console because its super buggy, just run `python main.py` in shell and resize the terminal). Then, run `viu` and select yes at the installation prompt.

If you're NOT using Replit, just run it as normal. Run `pip install -r requirements.txt` (maybe pip3?) to install dependencies. You'll need to have `viu` (images in the terminal) installed (idk if the script will fail, but if the script doesn't die, then you can just check /tmp/captcha.png for the captcha if it's convienient.

Your accounts MAY disable if you create too many with one IP (not tested, just a guess). You should use some kind of proxy, idk.

TODO:
1. Automatically check inbox every 1 second instead of checking once every 25 seconds, to have smaller wait times.

--
ading2210 - freedns-client

doxr - reversing sharklasers and making the account alt creator
