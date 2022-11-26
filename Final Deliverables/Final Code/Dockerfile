#Create a ubuntu base image with python 3 installed.
FROM python:3

LABEL maintainer="Thirumalai Selvan, 1905120cse@cit.edu.in"
RUN apt-get update
RUN mkdir /app

#Set the working directory
WORKDIR /app

#copy all the files
COPY . /app

#Install the dependencies
RUN apt-get -y update
RUN pip3 install -r requirements.txt

#Expose the required port
EXPOSE 5000

ENTRYPOINT ["python"]
#Run the command
CMD [“python3”, “./app.py”]