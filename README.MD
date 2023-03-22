<img src="/assets/seeker-logo.png" alt="Seeker Logo">

# Seeker
## _Linux Digital Forensics toolkit written in Python and C_

## Features

- Automated data collection
- Data visualization
- IOC Detection using VirusTotal's API
- Web history analysis

## Built with

- [Streamlit](https://streamlit.io)
- [VirusTotal](http://virustotal.com)


## Setting up the data collection script

Clone the project

```bash
  git clone https://github.com/iikyc/seeker
```

Go to the project directory

```bash
  cd seeker/data_extractor/linux
```

Compile the C script

```bash
  gcc seeker.c -o seeker
```

Change permissions

```bash
  chmod +x seeker
```

Run the script

```bash
  ./seeker
```

## Setting up the web application

Clone the project

```bash
  git clone https://github.com/iikyc/seeker
```

Go to the project directory

```bash
  cd seeker/webapp
```

Install requirements

```bash
  pip install -r requirements.txt
```
or
```bash
  pip3 install -r requirements.txt
```

Setup .env file for VirusTotal API functionality

```bash
  echo VTKEY=YOUR_API_KEY > .env
```

Run the webapp

```bash
  streamlit run Main.py
```

## License
[MIT](https://github.com/iikyc/seeker/blob/master/LICENSE)
