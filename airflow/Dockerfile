FROM apache/airflow:2.5.0-python3.10

USER root

# Install OpenJDK-11
RUN apt update && \
    apt-get install -y openjdk-11-jdk && \
    apt-get install -y ant && \
    apt-get clean;

# Set JAVA_HOME
ENV JAVA_HOME /usr/lib/jvm/java-11-openjdk-amd64
RUN export JAVA_HOME
ENV PATH=$PATH:$JAVA_HOME/bin

ENV SPARK_VERSION=3.3.1
ENV HADOOP_VERSION=2.7.7

RUN chmod -R 777 /opt/

# download and install hadoop
RUN mkdir -p /opt && \
    cd /opt && \
    curl http://archive.apache.org/dist/hadoop/common/hadoop-${HADOOP_VERSION}/hadoop-${HADOOP_VERSION}.tar.gz | \
        tar -zx hadoop-${HADOOP_VERSION}/lib/native && \
    ln -s hadoop-${HADOOP_VERSION} hadoop && \
    echo Hadoop ${HADOOP_VERSION} native libraries installed in /opt/hadoop/lib/native

# download and install spark
RUN mkdir -p /opt && \
    cd /opt && \
    curl http://archive.apache.org/dist/spark/spark-${SPARK_VERSION}/spark-${SPARK_VERSION}-bin-hadoop2.tgz | \
        tar -zx && \
    ln -s spark-${SPARK_VERSION}-bin-hadoop2 spark && \
    echo Spark ${SPARK_VERSION} installed in /opt

ENV PATH $PATH:/opt/spark/bin
ENV SPARK_HOME /opt/spark/
RUN export SPARK_HOME

USER airflow


COPY requirements.txt .

RUN pip install -r requirements.txt

