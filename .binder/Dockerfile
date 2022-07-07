FROM rpy2/base-ubuntu:master-20.04

RUN apt-get update && apt-get install -y && rm -rf /var/lib/apt/lists/* && \
    R -e "install.packages('BiocManager')" && \
    R -e "BiocManager::install('rcellminer')" && \
    pip install --no-cache --upgrade pip && \
    pip install --no-cache notebook torch networkx pandas numpy requests
    
# create user with a home directory
ARG NB_USER
ARG NB_UID
ENV USER ${NB_USER}

RUN adduser --disabled-password \
    --gecos "Default user" \
    --uid ${NB_UID} \
    ${NB_USER}

COPY --chown=${USER} . ../notebook 
COPY --chown=${USER} . ../DrugCell
COPY --chown=${USER} . ../data
COPY --chown=${USER} . ../Hidden_sample
COPY --chown=${USER} . ../Result_sample 
WORKDIR notebook
USER ${USER}
