# base image
FROM openjdk:11

# define spark and hadoop versions
ENV SPARK_VERSION=3.3.1
ENV HADOOP_VERSION=2.7.7

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

# add scripts and update spark default config
ADD common.sh spark-master spark-worker /
ADD spark-defaults.conf /opt/spark/conf/spark-defaults.conf
ENV PATH $PATH:/opt/spark/bin
RUN wget https://jdbc.postgresql.org/download/postgresql-42.5.1.jar
RUN mv postgresql-42.5.1.jar /opt/spark/jars

# Set SPARK_HOME
ENV SPARK_HOME /opt/spark/
RUN export SPARK_HOME




