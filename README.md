# wp-plugin-checker
**A cross-platform python based utility to identity wordpress plugins used by a website.**

[![wpscan.png](https://s3.postimg.org/58liso0lf/wpscan.png)](https://postimg.org/image/58liso0lb/)

### Requirements

- Python 2
- Python `pip`
- Python module `requests`
- Python module `colorama`
- Python module `beautifulsoup`

### Install modules

	pip install -r requirements.txt
	
### Tested on

- Windows 7/8
- Kali linux (2017.1)

	 
### Download wp-plugin-checker

You can download the latest version of cbtnuggets-dl by cloning the GitHub repository.

	git clone https://github.com/r0oth3x49/wp-plugin-checker.git


### Usage 

***Check using default option***

	python wp-check.py -u https://www.abc.com -d
	
***Check using default option with tor proxy***

	python wp-check.py -u https://www.abc.com -d --tor
	
***Check using default option with tor proxy by requesting new identity***

	python wp-check.py -u https://www.abc.com -d --tor --new-identity
	
***Check using bruteforce option***

	python wp-check.py -u https://www.abc.com -b
	
***Check using bruteforce option by specifying threads***

	python wp-check.py -u https://www.abc.com -b -t 10
	
***Check using bruteforce option with tor proxy***

	python wp-check.py -u https://www.abc.com -b --tor
	
***Check using bruteforce option with tor proxy by requesting new identity***

	python wp-check.py -u https://www.abc.com -b --tor --new-identity
	
***Check using bruteforce option by providing custom wordlist***

	python wp-check.py -u https://www.abc.com -b -w "/path/to/wordlist/"
	

### Advanced Usage

<pre><code>
Author: Nasir khan (<a href="http://r0oth3x49.herokuapp.com/">r0ot h3x49</a>)

Usage: wp-check.py [OPTIONS] URL

Options:
  General:
    -h, --help         Print this help text and exit
    -v, --version      Print program version and exit

  Target:
    -u URL, --url=URL  Provide target url (e.g:- http://www.abc.com)

  Output:
    -s, --save         Stores plugins in file with target url name.

  Custom:
    -w, --wordlist     Provide plugin wordlist else it will use default.
    -t, --threads      Provide threads default threads = 2

  Proxy:
    --tor              Uses tor proxy network to send traffic through
    --new-identity     Automated request for new identity on ip blocked

  Enumeration:
    -d, --default      Analyzes plugins from source code
    -b, --bruteforce   Analyzes plugins using bruteforce
  
  Example:
	python wp-check.py -u https://www.abc.com -d
</code></pre>

