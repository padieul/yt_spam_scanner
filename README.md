# YtSpamScanner - a Text Analytics project.

## How to run and debug?

#### Frontend

1.  If container not already running: `docker compose up` 
    or right-click on docker-compose.debug.yml in **VS-Code** and choose "Compose Up"
2.  Execute launch configuration "Launch Chrome against localhost". Set breakpoints inside "frontend/src" if necessary.

#### Middleware

1.  If container not already running: `docker compose up` 
    or right-click on docker-compose.debug.yml in **VS-Code** and choose "Compose Up"
2.  Open `localhost:8000/docs` to access API. To debug, execute launch configuration "Python: Middleware Remote Attach". Set breakpoints inside "middleware/app" if necessary.

> Before running `docker compose up` on Windows computers, please make sure the line ending is `LF` instead of `CRLF` in VSCODE for the file `middleware/start.sh`


<p align="center">
  <img src="./images/LF_settings.jpg" />
</p>
<!-- ![alt text](./images/LF_settings.jpg) -->




## Project contributions:

Timeframe       | Angelina  | Vivian    | Abdulghani                                               | Paul
--------        | --------  | --------  | -------                                                  | ------
10.11 - 25.11   | Inhalt    | Inhalt    | Configuring Docker containers and compose                | Configuring ES and Kibana
26.11 - 02.12   | Inhalt    | Inhalt    | Preparing and uploading the data to Elasticsearch        | Experimenting with debug configurations involving multiple containers including Svelte, FastApi, TensorFlow Serving and bare Python projects.
