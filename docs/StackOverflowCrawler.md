# Stack Overflow Crawler
## Problem summary
During a meeting with Wojciech Jaworski PhD, we got an idea that it may be really helpful to create a Stack Overflow crawler, that will try to match log parts from user's questions with captured log.

1. Try to find automatically answer
2. Help with logs clustering

## Useful links
* https://api.stackexchange.com/docs - API of AskUbuntu among others.
* https://archive.org/details/stackexchange - 500 MB of AskUbuntu data.

## Proposed solution
Because API implements throttles, I don't see possible use for clustering in scalable system. On the other hand, there exists data dump with number of possible applications. Given error messages and labels in Stack Exchange dump, it seems easy to validate clustering algorithms with this large amount of data. There is also place for heuristic algorithms looking for the same key words - similarly to Mateusz's approach - and apply accepted answer.

Maybe there also could be question creator if error occurs often - but due to question quality restrictions and possible verification issues ([create question issues](https://api.stackexchange.com/docs/create-question)) it could only be semi-automatic and dpcs-team verified.
