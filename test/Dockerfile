FROM ncbi/edirect as edirect

RUN apt-get update && apt-get install -y --no-install-recommends  \
    python3.6   \
    python3-pip \
    git         \
  && rm -rf /var/lib/apt/lists/*  && \
     apt-get autoremove -y        && \
     apt-get clean


RUN pip3 install entrezpy
ENV ENTREZPY_DST /entrezpytest
ENV ENTREZPY_SRC https://gitlab.com/ncbipy/entrezpy.git
RUN git clone --branch 'master' $ENTREZPY_SRC $ENTREZPY_DST
CMD ["/bin/bash"]
