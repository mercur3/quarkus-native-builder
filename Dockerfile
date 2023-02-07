FROM fedora:__fedora_version__

# Configure =rpm=

# By default dnf is configured as a singletheaded application. This configuration aims to increase
# build speed as it spends less time doing I/O operations and connecting to the mirrors.
RUN rm /etc/dnf/dnf.conf
COPY dnf.conf /etc/dnf/

# Installing the dependencies

RUN dnf update --nodocs; \
    dnf install --nodocs gcc glibc-devel zlib-devel libstdc++-static freetype-devel; \

# install mandrel
    cd /opt; \
    curl \
        --output graalvm-quarkus.tar.gz \
        -L \
        https://github.com/graalvm/mandrel/releases/download/mandrel-__mandrel_version__/mandrel-java__java_version__-linux-amd64-__mandrel_version__.tar.gz; \
    tar -xvf graalvm-quarkus.tar.gz; \
    rm graalvm-quarkus.tar.gz; \

    export JAVA_HOME="$(pwd)/graalvm-quarkus"; \
    export GRAALVM_HOME="${JAVA_HOME}"; \
    export PATH="${GRAALVM_HOME}/bin:$PATH"; \

# clean up
    dnf clean all; \
    rm -rf /var/log /tmp;

