<svg xmlns="http://www.w3.org/2000/svg" viewBox="10 0 200 20" fill="none">
    <text x="12" y="15" fill="#ea4335">Under Construction</text>
</svg><br/>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="10 0 400 20" fill="none">
    <text x="12" y="15" fill="#ea4335">At the moment these instructions will not work.</text>
</svg><br/>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="10 0 400 20" fill="none">
    <text x="12" y="15" fill="#ea4335">We are working hard to change that.</text>
</svg>


## Recommended Steps to Get Started

To get the penetrometer recorder script running without user interaction after boot
its filename needs to be added to `/etc/rc.local`, and that file's executable
bit has to be set, if necessary.

The provided setup script installs the recorder file in `/opt/lava_vield_penetrometer/`.
This could be also pretty much any arbitrary folder on the system.  
- [ ] TODO: Check that data folder in recorder script is something reasonable,
  probably the pi home folder or maybe `/lfp/`.

1. Connect the Raspberry Pi to the network.
2. Check if `git` ([`git-scm.org`](https://git-scm.org)) is installed.
   ```bash
   git --version
   ```
   If there is some error message, or complaining about unknown command, git needs
   to be installed.
   ```bash
   apt install git
   ```
3. Clone this repository somewhere on the Raspberry Pi
   ```bash
   git clone https://github.com/LAVAPUBMH/Lava_Field_Penetrometer.git
   ```
4. Change into the folder that contains all RaspberryPi related files; then run
   the setup script:
   ```bash
   cd "Lava_Field_Penetrometer/Files For Raspi/"
   ./setup.sh
   ```
