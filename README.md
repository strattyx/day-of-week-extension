# Day of week extension
A quick and simple extension to demonstrate how 
- input: TZ database timezone
- output: Day of week

## Deployment
#### Hosting
This example assumes that you self-host the repo. We don't expect the usage of the extension to exceed free-tier requirements for most hosting platforms (ie - heroku). If this is still a problem contact [@dvtate](https://me.dvtate.com) and we can maybe host it on StrattyX servers.
#### Install Dependencies
You also need to have to have python3 and pip3 installed and configure your firewall to accept requests on port 5051 (can change this port number). 
```sh
sudo pip3 install flask, python-dateutil, pytz
```
#### Start extension
I also reccomend using a tool like [forever](https://github.com/foreversd/forever) to prevent any downtime due to unexpected errors.
```sh
python3 main.py
```
#### Link with StrattyX
We are currently only using extensions internally. Once we finish building out resources for procedureally generating form UI we will open the system up for 3rd party developers. Sorry for the delay.
###### Submission: 
- about extension: title, summary, etc. 
- URI: host we can use to call webhooks
- Parameters: for example to get a
- UI: desired form appearance 

## How it works
There is a more general extension documentiation repo coming soon

#### Timeline Rerturn value
- 'start' is equivalent to the timestamp at beginning of the period
- the value given remains until the next timestamp comes up
```json
{
    "start" : "Monday",
    "2001-1-1" : "Tuesday",
    "2001-1-2" : "Wednesday",
    ...
}
```
