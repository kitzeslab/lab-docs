# Computing resources setup

## SSH into `robin`: 
Our lab computer, `robin`, can be used for data storage and small analyses. If you don't already have an account, create one by logging into your Pitt computing account while physically sitting at `robin` (not via SSH).

We will also have to ask for you to be added to the JMR-USER VPN role.


To SSH, 
1. Get onto the JMR-USER VPN using Pulse Secure. (You'll have to select the JMR-USER role.) :

   * Download Pulse Secure
   * Make a new connection named "Pitt VPN" with server `sremote.pitt.edu`.
   * Connect to the connection. Read the instructions on which secondary password to use for Duo authentication
   * Enter your Pitt username and password.
   * Select the JMR-USER Lab role after completing the Duo login
   
2. SSH into `robin` with the lab username:

        ssh <username>@robin.<rest of domain name>

3. Enter your password for your account on `robin` when prompted.

## Configuring an SSH alias
If the idea of typing in a long address every time you SSH doesn't excite you, it's easy to set up a simple SSH alias so that you can log in with the command `ssh robin`.

1. Open (or create) an SSH config file, `~/.ssh/config` on your local machine (i.e. the one you're sitting at). Use whatever text editor you're familiar with, or `nano` if you're not sure what to use.

        nano ~/.ssh/config

2. Insert these lines with your own Phoebe username after `User`, and the correct domain name for HostName. Note that each indented line must be tabbed, not spaced

        Host robin
                HostName %h.<rest of domain name>
                ForwardX11 yes
                ForwardX11Trusted yes
                Compression yes
                User <username>


3. Now write your file and exit back to the terminal.

### Configure an SSH keypair
If you also don't want to type in a password every time you log in, you can set up an automatic login from your personal laptop using a keypair. (Only do this if you're certain your personal computer is secure!)

1. If you don't already have one, generate a keypair by running this command, then pressing `return` 3x:

        ssh-keygen

2. Mac users: install [Homebrew](https://brew.sh/) if you haven't already 

3. Install `ssh-copy-id`, then use it to copy the public key to your home directory on the remote machine

        brew install ssh-copy-id
        ssh-copy-id -i ~/.ssh/id_rsa.pub phoebe
        
4. Type your account password when prompted

Now you can login by simply typing `ssh phoebe`.

## SSH into the CRC cluster:
The [Center for Research Computing](https://crc.pitt.edu/) has several clusters. We use the `h2p` cluster located at `h2p.crc.pitt.edu`. You need to be added to the cluster before you can access it.

1. Connect to the VPN for this also--just use the JMR-USER role.

2. SSH with your Pitt username at `h2p.crc.pitt.edu`, e.g.:

        ssh abc123@h2p.crc.pitt.edu

3. Enter your Pitt password when prompted.

4. Set up an SSH alias, if desired. Follow the instructions in the previous section but add these additional lines to your config file (with your own username):

        Host h2p
                HostName %h.crc.pitt.edu
                ForwardX11 yes
                ForwardX11Trusted yes
                Compression yes
                User abc123        

## Configuring cluster account
Actually accessing the computing nodes requires that you set up another key in your home folder at `h2p.crc.pitt.edu`. 

1. Log in to your `h2p` account, e.g.

        ssh h2p

2. Create a new keypair (& return 3x)

        ssh-keygen

3. Append the new public key to the list of authorized keys

        cat ~/.ssh/id_rsa.pub >> ~/.ssh/authorized_keys

Lastly, set yourself up a storage directory on the cluster.

4. Make a personal storage directory with your Pitt username within `/zfs1/jkitzes`

        mkdir /zfs1/jkitzes/abc123

You can check our lab's storage quota using `beegfs-ctl --getquota --gid jkitzes`.


## Configuring Ethernet

To configure internet on your computer, request an IP address by completing [this form](https://www.biology.pitt.edu/facilities/networking). 

Some tips on filling out this form: 
* The Ethernet Port Address is the 12-digit number on the wall port nearest your computer (it starts with "OCH").
* If your computer has a built-in Ethernet port, find the port's MAC address. Note that this is different from your computer's WiFi MAC address.
* If your computer does not have a built-in Ethernet port, you need an Ethernet adapter. Plug in your adapter and find its MAC address.
        * On an Apple computer, find the MAC address by opening the "Network Utility" program > clicking on "Info" > selecting the adapter in the drop-down menu. The "Hardware Address" listed here is the MAC address of your Ethernet port. 
