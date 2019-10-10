# Day of week extension
- Notice there are two webhook endpoints, one 'realtime' and one 'timeline'

## About this extension
- input: TZ database timezone
- output: Day of week


## Timeline
- 'start' is equivalent to the beginning of the period
```json
{
    "start" : "Monday",
    "2001-1-1" : "Tuesday",
    "2001-1-2" : "Wednesday",
    ...
}
```
