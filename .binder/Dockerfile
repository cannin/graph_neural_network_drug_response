FROM rocker/binder:4.2.0

# Copy your repository contents to the image
COPY --chown=rstudio:rstudio . ${HOME}

RUN if [ -f install.R ]; then R --quiet -f install.R; fi && \
    pip install --user numpy pandas torch networkx
