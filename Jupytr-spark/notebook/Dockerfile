FROM itayb/spark:3.1.1-hadoop-3.2.0

COPY requirements.txt .
RUN pip3 install -r requirements.txt


# install extension to monitor spark
RUN jupyter nbextension install sparkmonitor --py --user --symlink
RUN jupyter nbextension enable  sparkmonitor --py
RUN jupyter serverextension enable --py --user --debug sparkmonitor
RUN ipython profile create && \
echo "c.InteractiveShellApp.extensions.append('sparkmonitor.kernelextension')" >>  $(ipython profile locate default)/ipython_kernel_config.py

RUN apt-get --allow-releaseinfo-change-suite update
RUN apt-get install wget -y
RUN ln -s /usr/local/lib/python3.8/site-packages/sparkmonitor/listener_2.12.jar /opt/spark/jars/listener_2.12.jar
RUN wget https://jdbc.postgresql.org/download/postgresql-42.2.5.jar 
RUN mv postgresql-42.2.5.jar /opt/spark/jars/
#RUN apt-get -q -y install maven
#COPY pom.xml .
#RUN mvn dependency:resolve -f pom.xml
RUN wget https://repo1.maven.org/maven2/com/databricks/spark-xml_2.12/0.14.0/spark-xml_2.12-0.14.0.jar
RUN mv spark-xml_2.12-0.14.0.jar /opt/spark/jars/

RUN wget https://repo1.maven.org/maven2/org/apache/hadoop/hadoop-aws/3.2.0/hadoop-aws-3.2.0.jar
RUN mv hadoop-aws-3.2.0.jar /opt/spark/jars/

RUN wget https://repo1.maven.org/maven2/com/amazonaws/aws-java-sdk-bundle/1.11.375/aws-java-sdk-bundle-1.11.375.jar
RUN mv aws-java-sdk-bundle-1.11.375.jar /opt/spark/jars/

RUN wget https://repo1.maven.org/maven2/io/lakefs/hadoop-lakefs-assembly/0.1.9/hadoop-lakefs-assembly-0.1.9.jar 
RUN mv hadoop-lakefs-assembly-0.1.9.jar /opt/spark/jars/

VOLUME /home/notebook/

CMD jupyter notebook --port=8888 --ip=0.0.0.0 --no-browser --allow-root --NotebookApp.token='' --notebook-dir=/home/notebook/

