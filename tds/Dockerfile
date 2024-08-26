ARG USE_LOCAL_WAR=false

FROM unidata/tomcat-docker:10-jdk17 AS base

LABEL org.opencontainers.image.authors="Unidata"

USER root

# tds envs
ENV TDS_CONTENT_ROOT_PATH=/usr/local/tomcat/content
ENV THREDDS_XMX_SIZE=4G
ENV THREDDS_XMS_SIZE=4G
ENV THREDDS_WAR_URL=https://downloads.unidata.ucar.edu/tds/5.6/thredds-5.6-SNAPSHOT.war

COPY files/setenv.sh ${CATALINA_HOME}/bin/setenv.sh
COPY files/javaopts.sh ${CATALINA_HOME}/bin/javaopts.sh
COPY files/server.xml ${CATALINA_HOME}/conf/

# Install necessary packages
RUN apt-get update && \
    apt-get install -y --no-install-recommends  vim build-essential m4 \
        libpthread-stubs0-dev libcurl4-openssl-dev gosu zip unzip && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# thredds: either copy local war file or curl one from THREDDS_WAR_URL
FROM base AS use-local-war-true
COPY local-war-file/*.war thredds.war

FROM base AS use-local-war-false
RUN curl -fSL "${THREDDS_WAR_URL}" -o thredds.war

FROM use-local-war-${USE_LOCAL_WAR} AS final
RUN unzip thredds.war -d ${CATALINA_HOME}/webapps/thredds/ && \
    rm -f thredds.war && \
    mkdir -p ${CATALINA_HOME}/content/thredds && \
    chmod 755 ${CATALINA_HOME}/bin/*.sh && \
    mkdir -p ${CATALINA_HOME}/javaUtilPrefs/.systemPrefs

EXPOSE 8081 8443

WORKDIR ${CATALINA_HOME}

# Inherited from parent container
ENTRYPOINT ["/entrypoint.sh"]

# Start container
CMD ["catalina.sh", "run"]

HEALTHCHECK --interval=10s --timeout=3s \
    CMD curl --fail 'http://localhost:8081/thredds/catalog.html' || exit 1
