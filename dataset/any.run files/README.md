any.run (https://any.run/) is an online sandbox service with both free and paid plans.  Its service is unique in that it allows interaction with virtual machines, rather than the simple automatic execution offered by most other sandboxes.  This interaction is useful since it allows real-time monitoring of samples to see network activity.

Samples are pulled from MalShare (https://malshare.com/).  I customized use of the API endpoints so that the downloaded file type could be specified.  Pe32 files produce the most pcaps, so I went with those for download.  I also account for API limits so there are no error files (text files that inform you that you have reached your API limit) included.  You can see the tools I used in the tools folder, as well as a record of each sample's hash and other information.

After samples are pulled, they are scanned using VirusTotal (https://www.virustotal.com/gui/home/upload).  The purpose of this scanning is to filter samples.  Malware samples that are marked as malicious by <10 antivirus softwares represented by VirusTotal are not tested on any.run.

Each sample is allowed to run for a minimum of 120 seconds in any.run.  If no network activity is registered, then I moved on to the next sample; if network activity is registered, I allowed the sample to run for 5 minutes.  Thus the pcap files represented here were allowed to run for 5 minutes.  Each sample was run on a 32-bit Windows 7 machine with full internet access.

I save all of the sample files, including those that didn't pass the filtering stage.  any.run also keeps track of each analysis, so I can go back and look at each analysis again and re-download pcap files.
