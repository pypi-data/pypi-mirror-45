# pepsepy Module Repository

## Table of Contents

- [pepsepy Module Repository](#pepsepy-module-repository)
  - [Table of Contents](#table-of-contents)
  - [GIT](#git)
  - [Create master branch and push it to server](#create-master-branch-and-push-it-to-server)
  - [Collaborating](#collaborating)
    - [Create a new branch](#create-a-new-branch)
    - [Git Branching - Rebasing](#git-branching---rebasing)
      - [Basic Branching and Merging](#basic-branching-and-merging)
        - [Simple workflow](#simple-workflow)
        - [Basic merge conflicts](#basic-merge-conflicts)
      - [Basic rebasing](#basic-rebasing)
  - [Structure of the Repository](#structure-of-the-repository)
  - [Install](#install)
  - [Install using pip](#install-using-pip)
  - [Uninstall](#uninstall)
  - [To-do](#to-do)
  - [GitLab CI/CD: GitLab Continuous Integration](#gitlab-cicd-gitlab-continuous-integration)
    - [Continuous Integration](#continuous-integration)
    - [Continuous Delivery](#continuous-delivery)
    - [Continuous Deployment](#continuous-deployment)
    - [How GitLab CI/CD (or travis CI) works](#how-gitlab-cicd-or-travis-ci-works)
      - [Git - taging](#git---taging)

This simple project is an example repo for Python projects.

Learn more <http://www.kennethreitz.org/essays/repository-structure-and-python>

git clone https://gitlab.com/vlle-cenaero/pepsepy.git

cd pepsepy

python setup.py install [--record files.txt]

## GIT

Command line instructions

Git global setup
git config --global user.name "Van Long Lê"
git config --global user.email "vanlong.le@cenaero.be"

Create a new repository
git clone https://gitlab.com/vlle-cenaero/pepsepy.git
cd pepsepy
touch README.md
git add README.md
git commit -m "add README"
git push -u origin master

Existing folder
cd existing_folder
git init
git remote add origin https://gitlab.com/vlle-cenaero/pepsepy.git
git add .
git commit -m "Initial commit"
git push -u origin master

Existing Git repository
cd existing_repo
git remote rename origin old-origin
git remote add origin https://gitlab.com/vlle-cenaero/pepsepy.git
git push -u origin --all
git push -u origin --tags

## Create master branch and push it to server

git init

git remote add origin http://gitlab.com/vlle-cenaero/pepsepy.git

Make changes ...

git add files folders

git commit -m "messages"

git push origin master

## Collaborating

### Create a new branch

git checkout -b pepseday2019

add and commit

git push -u origin new_branch: push to server

invite new collaborators

For new collaborators:

git clone http://gitlab.com/vlle-cenaero/pepsepy.git

git checkout --track origin/pepseday2019

make changes

git add . && git commit

git fetch or git pull

solve conflicts

git push -u origin pepseday2019

The conflicts comme here

git push -u [--set-upstream] origin pepseday2019

The next step is to see how to merge pepseday2019 to master

Case: work on pepseday2019, the work is done and readay to merge it backt to master

(--rebase will get the changes from master and could overwrite changes other people made)

The goal is to keep pepseday2019 branch updated with the things happening in master and later could merge them back into master
No, rebase never overwrite, it just trying to achieve a cleaner history, by reattach (or fake) the history to the late point of the master. (it undoes the commits from the branch pepseday2019, then applies the commit backt to )

### Git Branching - Rebasing

In Git, there are two main ways to integrate changes from one branch into another: the **merge** and the **rebase**.

The easiest way to integrate the branches, as we’ve already covered, is the merge command. It performs a three-way merge between the two latest branch snapshots (C3 and C4) and the most recent common ancestor of the two (C2), creating a new snapshot (and commit).

![altext](https://git-scm.com/book/en/v2/images/basic-rebase-2.png)

#### Basic Branching and Merging

##### Simple workflow

1. Do some work on a website (git add, git commit)
2. Create a branch for a new user story you're working on (git checkout -b new_branch)
3. Do some work in that branch (git commit -a -m 'added a new footer [issue 53]')

At this stage, you’ll receive a call that another issue is critical and you need a hotfix. You’ll do the following:

Note: when you’ve been working on part of your project, things are in a messy state and you want to switch branches for a bit to work on something else. The problem is, you don’t want to do a commit of half-done work just so you can get back to this point later. The answer to this issue is the `git stash` command.

```Git
git status

Changes to be commited
...

git stash
Saved working directory and index state
...

git status
# On branch master
nothing to commit, working directory clean
```

At this point, you can switch branches and do work elsewhere; your changes are stored on your stack. To see which stashes you’ve stored, you can use git stash list:

`git stash list`

`git stash apply` (most recent) or `git stash apply stash@{2}` (specific stash)

1. Switch to your production (git checkout master)
2. Create a branch to add hotfix (git checkout -b hotfix)
3. After it is tested, merge the hotfix branch, and push to production (git commit -a -m 'fixed the broken email address')
4. Switch back to your original user story and continue working (git checkout master, git merge hotfix)

After your super-important fix is deployed, you’re ready to switch back to the work you were doing before you were interrupted. However, first you’ll delete the hotfix branch, because you no longer need it — the master branch points at the same place. You can delete it with the -d option to git branch:

git branch -d hotfix

Now you can switch back to your work-in-progress branch on issue #53 and continue working on it.

```Git
git checkout iss53
vim index.html
git commit -a -m 'finished the new footer [issue 53]'
```

It is worth noting here that the work you did on your hotfix branch is not contained in the files in your iss53 branch. If you need to pull it in, you can merge your master branch into your iss53 branch by running `git merge master`, or you can wait to integrate those changes untill you decide to pull the iss53 branch back into master later

The issue #53 is commplete and ready to be merged into your master branch.

```Git
git checkout master
git merge iss53
```

##### Basic merge conflicts

For resolving the merge conflict, you can run git mergetool, which files up an appropriate visual merge tool and walks you through the conflicts

#### Basic rebasing

There is another way to integrate the branches: you can take the patch of the change that was introduced

---------------

If you want to learn more about `setup.py` files, check out `this repository <https://github.com/kennethreitz/setup.py>`_.

## Structure of the Repository

- README.md
- LICENSE
- setup.py
- requirements.txt
- pepsepy/__init__.py
- pepsepy/core.py
- pepsepy/util.py
- docs/conf.py
- docs/index.md

## Install

python setup.py install
or
python setup.py install --record files.txt : To record a list of installed files

## Install using pip

## Uninstall

Linux: xargs rm -rf < files.txt or cat files.txt | xargs rm -rf
Windows: using Powershell
Get-Content files.txt | ForEach-Object {Remove-Item $_ -Recurse -Force}
Then delete also the containing directory: ~/Programs/anaconda/.../pepsepy

## To-do

- merge pepseday2019 to master
- create release entries
- create changelog
- create wiki
- create CONTRIBUTING.md
- create gitlab CI/CD
  
## GitLab CI/CD: GitLab Continuous Integration

The continuous methodologies of software development are based on automating the execution of scripts to
minimize the chance of introducing errors while developing applications. They require less human
intervention or event no intervention at all, from the develoment of new code until its deployment.

It involves continuously building, testing, and deploying code changes at every small iteration, reducing
the chance of developing new code cased on bugged or failed previous versions

### Continuous Integration

Developers push code changes every day, multiple times a day. For every push to the repository, you can create a set of scripts to build and test your application automatically, decreasing the chance of introducing errors to your app.

This practice is known as Continuous Integration; for every change submitted to an application - even to development branches - it’s built and tested automatically and continuously, ensuring the introduced changes pass all tests, guidelines, and code compliance standards you established for your app.

### Continuous Delivery

 Continuous Delivery is a step beyond Continuous Integration. Your application is not only built and tested at every code change pushed to the codebase, but, as an additional step, it’s also deployed continuously, though the deployments are triggered manually.

This method ensures the code is checked automatically but requires human intervention to manually and strategically trigger the deployment of the changes.

### Continuous Deployment

 Continuous Deployment is also a further step beyond Continuous Integration, similar to Continuous Delivery. The difference is that instead of deploying your application manually, you set it to be deployed automatically. It does not require human intervention at all to have your application deployed.

- GitLab's built-in tool for sofware development using continuous methodology
  - Continuous integration (CI)
  - Continuous delivery and deployment (CD)

![altext](https://docs.gitlab.com/ee/img/devops-stages.png)

### How GitLab CI/CD (or travis CI) works

 To use GitLab CI/CD, all you need is an application codebase hosted in a Git repository, and for your build, test, and deployment scripts to be specified in a file called .gitlab-ci.yml, located in the root path of your repository.

In this file, you can define the scripts you want to run, define include and cache dependencies, choose commands you want
to run in sequence and those you want to run in parallel, define where you want to deploy your app, and specify whether
you will want to run the scripts automatically or trigger any of them manually. Once you’re familiar with GitLab CI/CD you
can add more advanced steps into the configuration file.

To add scripts to that file, you’ll need to organize them in a sequence that suits your application and are in accordance with the tests you wish to perform. To visualize the process, imagine that all the scripts you add to the configuration file are the same as the commands you run on a terminal in your computer.

Once you’ve added your .gitlab-ci.yml configuration file to your repository, GitLab will detect it and run your scripts with the tool called GitLab Runner, which works similarly to your terminal.

The scripts are grouped into jobs, and together they compose a pipeline. A minimalist example of .gitlab-ci.yml file could contain:

before_script:

    - apt-get install rubygems ruby-dev -y

run-test:

    script:

        - ruby --version

The before_script attribute would install the dependencies for your app before running anything, and a job called run-test would print the Ruby version of the current system. Both of them compose a pipeline triggered at every push to any branch of the repository.

GitLab CI/CD not only executes the jobs you’ve set, but also shows you what’s happening during execution, as you would see in your terminal:

![altext](https://docs.gitlab.com/ee/ci/introduction/img/job_running.png)

![altext](https://docs.gitlab.com/ee/ci/introduction/img/gitlab_workflow_example_11_9.png)

source: https://docs.gitlab.com/ee/ci/introduction/index.html

#### Git - taging

delete local tag '12345'

`git tag -d 12345`

delete remote tag '12345' (eg, GitHub version too)

`git push origin :refs/tags/12345`

alternative approach

`git push --delete origin tagName`

`git tag -d tagName`
