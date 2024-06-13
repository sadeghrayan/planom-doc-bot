# app/Dockerfile

FROM node:16-alpine as build-step
WORKDIR /app
ENV PATH /node_modules/.bin:$PATH
COPY frontend ./frontend
RUN rm -rf /app/frontend/node_modules
RUN cd frontend && yarn install
RUN cd frontend && REACT_APP_API_HOST=/api yarn build

FROM python:3.9-slim

WORKDIR /app
RUN mkdir -p ./frontend/build
COPY --from=build-step ./app/frontend/build ./frontend/build 
RUN mkdir ./api
RUN mkdir ./data

RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    git \
    && rm -rf /var/lib/apt/lists/*


COPY api ./api
COPY data ./data
COPY requirements.txt ./requirements.txt
#COPY boto3-1.24.45-py3-none-any.whl ./boto3-1.24.45-py3-none-any.whl
#COPY nvidia_cufft_cu12-11.0.2.54-py3-none-manylinux1_x86_64.whl ./nvidia_cufft_cu12-11.0.2.54-py3-none-manylinux1_x86_64.whl
#COPY nvidia_cusparse_cu12-12.4.1.24-py3-none-manylinux2014_x86_64.whl ./nvidia_cusparse_cu12-12.4.1.24-py3-none-manylinux2014_x86_64.whl
#COPY nvidia_cusolver_cu12-11.4.5.107-py3-none-manylinux1_x86_64.whl ./nvidia_cusolver_cu12-11.4.5.107-py3-none-manylinux1_x86_64.whl
#COPY nvidia_cublas_cu12-12.5.2.13-py3-none-manylinux2014_x86_64.whl ./nvidia_cublas_cu12-12.5.2.13-py3-none-manylinux2014_x86_64.whl
#COPY nvidia_cudnn_cu12-8.9.2.26-py3-none-manylinux1_x86_64.whl ./nvidia_cudnn_cu12-8.9.2.26-py3-none-manylinux1_x86_64.whl
#COPY nvidia_nccl_cu12-2.20.5-py3-none-manylinux2014_x86_64.whl ./nvidia_nccl_cu12-2.20.5-py3-none-manylinux2014_x86_64.whl
#COPY triton-2.3.0-cp39-cp39-manylinux_2_17_x86_64.manylinux2014_x86_64.whl ./triton-2.3.0-cp39-cp39-manylinux_2_17_x86_64.manylinux2014_x86_64.whl
#COPY nvidia_cusparse_cu12-12.1.0.106-py3-none-manylinux1_x86_64.whl ./nvidia_cusparse_cu12-12.1.0.106-py3-none-manylinux1_x86_64.whl
#COPY torch-2.3.0-cp39-cp39-manylinux1_x86_64.whl ./torch-2.3.0-cp39-cp39-manylinux1_x86_64.whl
#COPY nvidia_cublas_cu12-12.1.3.1-py3-none-manylinux1_x86_64.whl ./nvidia_cublas_cu12-12.1.3.1-py3-none-manylinux1_x86_64.whl

#RUN pip3 install ./boto3-1.24.45-py3-none-any.whl
#RUN pip3 install ./nvidia_cufft_cu12-11.0.2.54-py3-none-manylinux1_x86_64.whl
#RUN pip3 install ./nvidia_cusparse_cu12-12.4.1.24-py3-none-manylinux2014_x86_64.whl
#RUN pip3 install ./nvidia_cublas_cu12-12.5.2.13-py3-none-manylinux2014_x86_64.whl -vvv
#RUN pip3 install ./nvidia_cusolver_cu12-11.4.5.107-py3-none-manylinux1_x86_64.whl -vvv
#RUN pip3 install ./nvidia_cublas_cu12-12.5.2.13-py3-none-manylinux2014_x86_64.whl -vvv
#RUN pip3 install ./nvidia_cudnn_cu12-8.9.2.26-py3-none-manylinux1_x86_64.whl -vvv
#RUN pip3 install ./nvidia_nccl_cu12-2.20.5-py3-none-manylinux2014_x86_64.whl -vvv
#RUN pip3 install ./triton-2.3.0-cp39-cp39-manylinux_2_17_x86_64.manylinux2014_x86_64.whl -vvv
#RUN pip3 install ./nvidia_cusparse_cu12-12.1.0.106-py3-none-manylinux1_x86_64.whl -vvv
#RUN pip3 install ./nvidia_cublas_cu12-12.1.3.1-py3-none-manylinux1_x86_64.whl -vvv
#RUN pip3 install ./torch-2.3.0-cp39-cp39-manylinux1_x86_64.whl -vvv
RUN pip3 install -r ./requirements.txt -vvv
#RUN pip3 install ./torch-2.3.0-cp39-cp39-manylinux1_x86_64.whl
ENV FLASK_ENV production

EXPOSE 4000
WORKDIR /app/api
CMD [ "python3", "-m" , "flask" , "--debug" , "run", "--host=0.0.0.0", "--port=4000" ]
