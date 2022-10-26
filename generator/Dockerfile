FROM nvidia/cuda:11.7.0-devel-ubuntu22.04
RUN apt-get update
RUN apt-get install wget -y
RUN mkdir -p /root/miniconda3
RUN wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O /root/miniconda3/miniconda.sh
RUN sh /root/miniconda3/miniconda.sh -b -u -p /root/miniconda3
ENV PATH /root/miniconda3/bin:$PATH
RUN conda init bash
RUN conda update -n base -c defaults conda
COPY environment.yml environment.yml
RUN conda env create -f environment.yml
ENV PATH /root/miniconda3/envs/oneforall/bin:$PATH
RUN /bin/bash -c "source activate oneforall"
RUN which python
RUN pip install flatten-dict
# RUN conda install pytorch torchvision torchaudio cudatoolkit=11.6 -c pytorch -c conda-forge -y
RUN pip install torch torchvision torchaudio --extra-index-url https://download.pytorch.org/whl/cu116
COPY . .
ENTRYPOINT ["python", "generator.py"]
