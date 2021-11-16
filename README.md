# nexus

## Contents
1. [About](#1-about)
2. [Team](#2-team)
4. [Issues](#3-issues)
5. [Setup](#4-setup)

___

#### 1. About
COMS - W4156 ADVANCED SOFTWARE ENGINEERING group project.

___

#### 2. Team

Name | UNI | GitHub ID
-----|-----| -----
Nihar Maheshwari | nm3223 | [@niharmaheshwari](https://github.com/niharmaheshwari)
Shantanu Jain | slj2142 | [@shantanu-jain-2142](https://github.com/shantanu-jain-2142)
Talya Koschitzky | tk2892 | [@tykosc](https://github.com/tykosc)
Vaibhav Goyal | vg2498 | [@vaibhav12345](https://github.com/vaibhav12345)

___

#### 3. Issues
Check [this](https://github.com/niharmaheshwari/nexus/issues) for active development tickets and issues.

#### 4. Tests
**Steps for running unit tests and coverage**
For running individual tests:
```
python3 -m unittest -v <test-module-path>
```

For running coverage:
```
coverage run -m unittest discover
```

For generating html report:
```
coverage html --omit="**/Library/*,*__init__.py" -d test/coverage
```
The above command generates a report in the `test` forlder.

#### 5. Build and Run the service
**Steps for building and running the nexus service**
1. ssh to the ec2 server "3.135.193.250"
2. Login to the user nexus using the password 'nexus' without quotes
```
sudo su nexus
```
3. Switch to home directory
```
cd ~
```
4. Run the following commands, when prompted for ssh password enter "nexus123" without quotes
```
source env/bin/activate
tmux kill-server
tmux
./deploy.sh
```
