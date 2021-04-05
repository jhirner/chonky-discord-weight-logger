# set base image (host OS)
FROM python:3.8-slim-buster

# set the working directory in the container
WORKDIR /code

# copy the dependencies file to the working directory
COPY requirements.txt .

# install dependencies
RUN pip install -r requirements.txt

# copy the content of the local source directory to the working directory
COPY source/ .

# Make the startup script executable.
RUN chmod a+x launch-chonky.sh

# command to run on container start
CMD ["./launch-chonky.sh"]
