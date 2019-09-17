# Table of contents
* [Initial setup](#initial-setup)
* [Pull upstream changes](#pull-upstream-changes)
* [Developing with branches](#developing-with-branches)


# Initial setup

Make a GitHub account and make sure you have Git installed on your computer

Make a folder for repositories in your home folder on whatever place you're setting up Git--for instance, you'll probably want to set up some repositories on `phoebe`. 

Create a folder to keep your git repositories organized, e.g. 
one called `~/Repositories` or `~/Code`.

Set up an SSH key if you want: 
* On github.com, go to your Settings > SSH and GPG keys
* Copy your public key from `~/.ssh/id_rsa.pub` (create key with `ssh-keygen`)
* Find the SSH url of your repository by clicking on the "clone" button in the repo and "Use SSH" in the upper right corner of the dialogue box
* Change the url of your origin to the SSH url using `git remote set-url origin <new_url>`

# TODO

Rewrite this with the following instructions:
* How to clone 
* How to stay up-to-date
* How to switch branches
* How to push your changes


## Learn the basics

Follow [Justin's lesson on Git](http://datasci.kitzes.com/lessons/git/) if you are a first-time user, or need a refresher on how to use Git.

[back to top](#table-of-contents)
# Pull changes


[back to top](#table-of-contents)
# Developing with branches

If you're working on an ongoing bug fix or new feature implementation, use a separate, descriptively named branch. 
This helps to:
* Keep track of all the changes happening in one project
* Allow for testing of the feature/fix while keeping a standard version of the code around

In general, the workflow is as follows: 
* Make a branch for your feature off of the `develop` branch
* Build the feature, committing to the feature branch as it is built
* Then, submit a pull request (PR) to the `develop` branch
* Once the PR is merged/accepted, delete your feature branch

### Helpful commands

Check the available branches and see which one you're on:

```
$ git branch
```

Create or switch to a branch:

```
# Create and switch to branch
$ git checkout -b <new_branch_name>

# OR: switch to a branch that's already created
$ git checkout <branch_name>
```


### Workflow


1. Create a feature branch off the `develop` branch:

```
git checkout -b <feature_branch_name> develop
```

2. Start making changes that are relevant to the branch 

3. Commit your changes with a descriptive message.

```
$ git add <files_you_modified>
$ git commit -m "<descriptive_message>"
```

4. Push your changes to a (new) branch on the remote:

```
$ git push -u origin <your_branch_name>
```

5. Go to github.com, create a pull request to the `develop` branch (not `master`!)

6. Make any more necessary changes to the pull request 

7. Once the feature is complete, merge the PR and delete the branch on github.com

8. Switch out of your local feature branch into `develop`, delete the local feature branch, and pull your merged changes:

```
$ git checkout develop
$ git branch -d <your_branch_name>
$ git pull 
```