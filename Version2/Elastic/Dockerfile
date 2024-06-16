ARG VERSION

FROM elasticsearch:${VERSION} AS Baseline

FROM openjdk:17-jdk-buster

ARG VERSION
ARG HTTP_PROXY
ARG HTTPS_PROXY
ENV VERSION=${VERSION}

USER root
WORKDIR /crack

COPY --from=Baseline /usr/share/elasticsearch/lib /usr/share/elasticsearch/lib
COPY --from=Baseline /usr/share/elasticsearch/modules/x-pack-core /usr/share/elasticsearch/modules/x-pack-core
COPY build_crack_jar.sh /crack
RUN mkdir output
RUN chmod 777 -R output 
RUN apt update && apt install -y zip
RUN bash build_crack_jar.sh
RUN cp LicenseVerifier.* ./output && cp XPackBuild.* ./output && cp x-pack-core* ./output

#CMD [ "bash", "build_crack_jar.sh" ]
