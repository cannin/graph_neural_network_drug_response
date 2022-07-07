FROM rpy2/base-ubuntu:master-21.10

RUN pip install --no-cache --upgrade pip && \
    pip install --no-cache notebook torch networkx pandas numpy requests && \
    R -e "install.packages('BiocManager')" && \
    R -e "BiocManager::install('rcellminer')"
  
# create user with a home directory
ARG NB_USER
ARG NB_UID
ENV USER ${NB_USER}

RUN adduser --disabled-password \
    --gecos "Default user" \
    --uid ${NB_UID} \
    ${NB_USER}

COPY --chown=${USER} . ../notebook 
COPY --chown=${USER} . ../data
WORKDIR notebook
USER ${USER}
